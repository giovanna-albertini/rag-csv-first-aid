# Configurações do projeto via variáveis de ambiente
from dataclasses import dataclass
import os

@dataclass
class Settings:
    openai_api_key: str = os.environ.get('OPENAI_API_KEY', '')
    embedding_model: str = os.environ.get('EMBEDDING_MODEL', 'text-embedding-3-small')
    llm_model: str = os.environ.get('LLM_MODEL', 'gpt-3.5-turbo')

settings = Settings()
