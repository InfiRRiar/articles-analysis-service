from langchain_openai import ChatOpenAI
from src.managers.qdrant_manager import QdrantManager


model = ChatOpenAI(
    name="gpt-4.1-2025-04-14",
    # name="gpt-4.1-mini",
    base_url="https://api.proxyapi.ru/openai/v1"
)

rag_qdrant_manager = QdrantManager("articles_rag")