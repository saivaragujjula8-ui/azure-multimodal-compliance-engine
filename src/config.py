from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    embedding_deployment: str = "text-embedding-3-small"
    chat_deployment: str = "gpt-4o-mini"
    azure_search_endpoint: str = ""
    azure_search_api_key: str = ""
    azure_search_index: str = "compliance-evidence"


def load_settings() -> Settings:
    load_dotenv()
    return Settings(
        azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
        azure_openai_api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
        embedding_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small"),
        chat_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4o-mini"),
        azure_search_endpoint=os.getenv("AZURE_SEARCH_ENDPOINT", ""),
        azure_search_api_key=os.getenv("AZURE_SEARCH_API_KEY", ""),
        azure_search_index=os.getenv("AZURE_SEARCH_INDEX", "compliance-evidence"),
    )
