import os
import pandas as pd
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
import json
import re
from typing import Optional
from api.config import Settings, get_settings
from api.logger import get_logger

class Azure_Document_Intelligence:
    def __init__(self):
        self.settings: Settings = get_settings()
        self.logger = get_logger(__name__)

    def read_doc(self, file_path: str) -> Optional[AnalyzeResult]:
        try:
            document_intelligence_client = DocumentIntelligenceClient(endpoint=self.settings.document_intelligence_endpoint, 
                                                                    credential=AzureKeyCredential(self.settings.document_intelligence_api_key)
                                                                    )

            # Leer el contenido del archivo
            with open(file_path, "rb") as f:
                poller = document_intelligence_client.begin_analyze_document(
                    model_id= self.settings.document_intelligence_model, 
                    analyze_request= f, 
                    content_type= "application/octet-stream", 
                    features= ["keyValuePairs"]
                )

            result: AnalyzeResult = poller.result()
            self.logger.info('Document readed successfully.')
            return result
        except Exception as e:
            self.logger.error(f'Error while reading docs. Error description: {str(e)}')
            return None
    
    def clean_text(self, text):
        text = text.replace('\n', ' ')
        text = re.sub(r'\s+', ' ', text)
        text = text.replace(':', '')
        text = text.strip()
        return text

    def key_value_pairs(self, result:AnalyzeResult) -> str:
        kv_dict = {}
        if result.key_value_pairs:
            for kv_pair in result.key_value_pairs:
                if kv_pair.key and kv_pair.value:
                    key = self.clean_text(kv_pair.key.content)
                    kv_dict[key] = kv_pair.value.content.encode("utf-8","ignore").decode("utf-8","ignore")
        kv = json.dumps(kv_dict)
        return kv
    
    def tables(self, result:AnalyzeResult) -> str:
        table_dict = {}
        for table_idx, table in enumerate(result.tables):
            aux_list = []
            for cell in table.cells:
                aux_dict = {}
                aux_dict['row'] = cell.row_index
                aux_dict['column'] = cell.column_index
                aux_dict['content'] = cell.content.encode("utf-8","ignore").decode("utf-8","ignore")
                if aux_dict['content'] != "":
                    aux_list.append(aux_dict)
            table_dict[table_idx] = aux_list
        table = json.dumps(table_dict)
        return table
    
    def get_center(self, polygon):
        x_coords = [polygon[i] for i in range(0, len(polygon), 2)]
        y_coords = [polygon[i+1] for i in range(0, len(polygon), 2)]
        center_x = sum(x_coords) / len(x_coords)
        center_y = sum(y_coords) / len(y_coords)
        return (center_x, center_y)
    
    def filter_paragraphs_not_in_tables(self, result):
        table_regions = []
        paragraphs = []
        # Recopilate regions with tables
        for table in result.get('tables', []):
            for cell in table.get('cells', []):
                for region in cell.get('boundingRegions', []):
                    table_regions.append(region)
        # Filter paragraphs not in tables
        for paragraph in result.get('paragraphs', []):
            in_table = False
            for region in paragraph.get('boundingRegions', []):
                for table_region in table_regions:
                    if (region['pageNumber'] == table_region['pageNumber'] and
                        region['polygon'][0] >= table_region['polygon'][0] and
                        region['polygon'][1] >= table_region['polygon'][1] and
                        region['polygon'][2] <= table_region['polygon'][2] and
                        region['polygon'][3] <= table_region['polygon'][3]):
                        in_table = True
                        break
                if in_table:
                    break
            if not in_table:
                paragraphs.append(paragraph)
        return paragraphs
    
    def paragraphs(self, result: AnalyzeResult) -> str:
        # Filter paragraphs not in tables
        filtered_paragraphs = self.filter_paragraphs_not_in_tables(result)
        # Extract the content and bounding regions
        texts = [(item['content'], item['boundingRegions'][0]['polygon']) for item in filtered_paragraphs]
        # Get centers for each text
        texts_with_centers = [(text, self.get_center(polygon)) for text, polygon in texts]
        # Sort texts by their y-coordinate (and then x-coordinate to handle lines)
        texts_with_centers.sort(key=lambda item: (item[1][1], item[1][0]))
        # Define the proximity threshold
        proximity_threshold_y = 25  
        proximity_threshold_x = 125  
        # Group texts that are close to each other
        grouped_texts = []
        current_group = []
        for i in range(len(texts_with_centers)):
            text, center = texts_with_centers[i]
            if not current_group:
                current_group.append((text, center))
            else:
                last_text, last_center = current_group[-1]
                if abs(center[1] - last_center[1]) < proximity_threshold_y and abs(center[0] - last_center[0]) < proximity_threshold_x:
                    current_group.append((text, center))
                else:
                    grouped_texts.append(current_group)
                    current_group = [(text, center)]
        if current_group:
            grouped_texts.append(current_group)
        # Consolidate the texts
        consolidated_text = '\n'.join([' '.join([text for text, center in group]) for group in grouped_texts])
        return consolidated_text  

    def format_result(self, result: AnalyzeResult) -> Optional[str]:
        try:
            # Paragraphs
            paragraphs = self.paragraphs(result)
            # Key value pairs
            kv = self.key_value_pairs(result)
            # Tables
            tables = self.tables(result)
            formated_result = f"""
                PARAGRAPHS:
                {paragraphs}
                KEY VALUE PAIRS:
                {kv}
                TABLES:
                {tables}
            """
            return formated_result
        except Exception as e:
            self.logger.error(f'Error while formating docs. Error description: {str(e)}')
            return None
        

    