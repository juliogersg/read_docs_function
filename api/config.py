import os
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path

SOURCE_DIR = Path(__file__).resolve().parents[1]
ENV_FILE: str = os.path.join(SOURCE_DIR, ".env")


class Settings(BaseSettings):
    # Document Intelligence
    document_intelligence_endpoint: str = Field(default="")
    document_intelligence_api_key: str = Field(default="")
    document_intelligence_model: str = Field(default="")

    # Azure OpenAI
    azure_openai_api_endpoint: str = Field(default="")
    azure_openai_api_version: str = Field(default="")
    azure_openai_model_deployment_name: str = Field(default="")
    azure_openai_model_deployment_name_vision: str = Field(default="")
    azure_openai_api_key: str = Field(default="")
    azure_openai_embeddings_deployment_name: str = Field(
        default="text-embedding-ada-002"
    )
    azure_openai_chat_temperature: float = Field(default=0.1)
    azure_openai_chat_completion_choices: int = Field(default=1)
    azure_openai_chat_presence_penalty: int = Field(default=2)
    azure_openai_chat_top_p: float = Field(default=1)

    #API
    assistant_api_key: str = Field(default="")
    assistant_api_origins: List[str] = Field(default=["http://localhost", "http://localhost:8080", "*"])


    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")

    def __init__(self, config_file: str = None, *args, **kwargs):
        super().__init__(_env_file=config_file or ENV_FILE, *args, **kwargs)


@lru_cache
def get_settings() -> Settings:
    """
    Returns a Settings object loaded with config properties from a .env file.
    The Settings object is allocated once in the memory and available during
    the application lifetime.
    """
    return Settings()
