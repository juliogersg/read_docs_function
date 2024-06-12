from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.utils.openai_functions import (
    convert_pydantic_to_openai_function,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_openai import ChatOpenAI
import httpx
from api.config import Settings, get_settings
from api.logger import get_logger

class Azure_OpenAI:
    def __init__(self):
        self.settings: Settings = get_settings()
        self.logger = get_logger(__name__)
    
    # def query(self, template: str, functions: str, function_name: str, ocr_content: str):
    #     try:
    #         template = template.replace("{ocr_content}", ocr_content, 1)
    #         prompt = ChatPromptTemplate.from_template(template)
    #         # # Create an HTTP client that does not verify SSL certificates
    #         # client = httpx.Client(verify=False)
    #         model = AzureChatOpenAI(
    #             openai_api_type='azure',
    #             openai_api_version=self.settings.azure_openai_api_version,
    #             azure_deployment=self.settings.azure_openai_model_deployment_name,
    #             azure_endpoint=self.settings.azure_openai_api_endpoint,
    #             openai_api_key=self.settings.azure_openai_api_key,
    #             # http_client= client,
    #         )
    #         # Build chain
    #         chain = (
    #             prompt
    #             | model.bind(function_call={"name": function_name}, functions=functions)
    #             | JsonOutputFunctionsParser()
    #         )
    #         # Invoke Azure OpenAI
    #         result = chain.invoke()
    #         print(chain.get_prompts())
    #         # Return
    #         self.logger.info('Query to OpenAI successfully completed')
    #         return result
    #     except Exception as e:
    #         self.logger.error(f'Error trying to query OpenAI. Error decription: {str(e)}')
    #         return None

    def query(self, template: str, functions, ocr_content: str):
        try:
            prompt = ChatPromptTemplate.from_template(template)
            model = AzureChatOpenAI(
                openai_api_type='azure',
                openai_api_version=self.settings.azure_openai_api_version,
                azure_deployment=self.settings.azure_openai_model_deployment_name,
                azure_endpoint=self.settings.azure_openai_api_endpoint,
                openai_api_key=self.settings.azure_openai_api_key,
            )
            # Build chain
            parser = JsonOutputFunctionsParser()
            chain = prompt | model.bind(functions=functions) | parser
            # Invoke Azure OpenAI
            result = chain.invoke({"ocr_content": ocr_content})
            # Return
            self.logger.info('Query to OpenAI successfully completed')
            return result
        except Exception as e:
            self.logger.error(f'Error trying to query OpenAI. Error decription: {str(e)}')
            return None

    def query_vision(self, template: str, functions, image_data):
        try:
            # prompt = ChatPromptTemplate.from_template(template)
            prompt = ChatPromptTemplate.from_messages(
                                                        [
                                                            ("system", f"{template}"),
                                                            (
                                                                "user",
                                                                [{"type": "image_url", "image_url": "data:image/jpeg;base64,{image_data}"}],
                                                            ),
                                                        ]
                                                    )
            model = AzureChatOpenAI(
                openai_api_type='azure',
                openai_api_version=self.settings.azure_openai_api_version,
                azure_deployment=self.settings.azure_openai_model_deployment_name_vision,
                azure_endpoint=self.settings.azure_openai_api_endpoint,
                openai_api_key=self.settings.azure_openai_api_key,
            )
            # Build chain
            parser = JsonOutputFunctionsParser()
            chain = prompt | model.bind(functions=functions) | parser
            # Invoke Azure OpenAI
            result = chain.invoke({"image_data": image_data})
            # Return
            self.logger.info('Query vision to OpenAI successfully completed')
            return result
        except Exception as e:
            self.logger.error(f'Error trying to query vision OpenAI. Error decription: {str(e)}')
            return None

