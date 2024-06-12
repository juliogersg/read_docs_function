import os
import re
import pandas as pd
import base64
from api.config import Settings, get_settings
from api.logger import get_logger
from api.utils.azure_openai import Azure_OpenAI
from api.utils.doc_intelligence import Azure_Document_Intelligence
from api.context.instructions import TEMPLATE_SS, TEMPLATE_PS
from api.models.output_models import payment_functions, salary_functions

class Orchestator:
    def __init__(self):
        self.settings: Settings = get_settings()
        self.logger = get_logger(__name__)
        self.azure_document_intelligence: Azure_Document_Intelligence = Azure_Document_Intelligence()
        self.azure_openai: Azure_OpenAI = Azure_OpenAI()

    def delete_file(self, file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)

    def process_payments(self, file_path: str) -> dict:
        try:
            # Read information from document
            doc_info = self.azure_document_intelligence.read_doc(file_path)
            doc_str = self.azure_document_intelligence.format_result(doc_info)
            # with open(r'C:\Users\julio\Downloads\strind_doc.txt', 'w') as archivo:
            #     archivo.write(doc_str)
            # Extract key information
            key_info = self.azure_openai.query(template=TEMPLATE_PS,
                                            functions=payment_functions,
                                            ocr_content=doc_str)
            return key_info
        except Exception as e:
            self.logger.error(f'Error processing payment schedules. Error decription: {str(e)}')
            return None
        
    def process_salary(self, file_path: str) -> dict:
        try:
            # Read information from document
            doc_info = self.azure_document_intelligence.read_doc(file_path)
            doc_str = self.azure_document_intelligence.format_result(doc_info)
            # Extract key information
            key_info = self.azure_openai.query(template=TEMPLATE_SS,
                                            functions=salary_functions,
                                            ocr_content=doc_str)
            key_info['net_salary'] = self.format_salary(key_info['net_salary'])
            return key_info
        except Exception as e:
            self.logger.error(f'Error processing salary slips. Error decription: {str(e)}')
            return None
        
    def process_salary_vision(self, file_path: str) -> dict:
        try:
            # Encode image
            image_data = self.encode_image(file_path)
            # Extract key information
            key_info = self.azure_openai.query_vision(template=TEMPLATE_SS,
                                                      image_data=image_data,
                                                      functions=salary_functions)
            return key_info
        except Exception as e:
            self.logger.error(f'Error processing salary slips. Error decription: {str(e)}')
            return None
        
    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
        
    def format_salary(self, value):
        try:
            # Eliminar espacios adicionales
            value = value.replace(' ', '')
            # Detectar formato con punto separando miles y coma decimales (caso específico)
            if re.match(r'^\d{1,3}(\.\d{3})*,\d{2}$', value):
                value = value.replace('.', '').replace(',', '.')
            else:
                # Eliminar todos los caracteres que no sean dígitos, comas o puntos
                value = re.sub(r'[^\d.,]', '', value)
                # Manejar el caso donde hay múltiples puntos (posiblemente separadores de miles incorrectos)
                if value.count('.') > 1:
                    value = value.replace('.', '', value.count('.') - 1)
                # Si hay tanto comas como puntos, asumir que las comas son separadores de miles
                if ',' in value and '.' in value:
                    value = value.replace(',', '')
                # Reemplazar comas por puntos para unificar los decimales si solo hay comas
                elif ',' in value and '.' not in value:
                    value = value.replace(',', '.')
            # Intentar convertir a float
            return str(value)
        except ValueError:
            return str(0.0)