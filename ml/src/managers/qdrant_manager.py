from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_openai.embeddings import OpenAIEmbeddings
from loguru import logger
from src.managers.chunk_manager import ArxivChunker
from qdrant_client.models import Filter
from uuid import uuid4
import os

table_name = "articles"

class QdrantManager():
    def __init__(self):
        self.client: QdrantClient = QdrantClient(":memory:")
        self.client.create_collection(
            collection_name=table_name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )
        
        self.embedder = OpenAIEmbeddings(
            model = "text-embedding-3-small",
            dimensions=1536,
            base_url="https://api.proxyapi.ru/openai/v1",
        )

        self.vectore_store: QdrantVectorStore = QdrantVectorStore(
            client=self.client,
            collection_name=table_name,
            embedding=self.embedder
        )
        

    def add_articles(self, documents):
        uuids = [str(uuid4()) for _ in range(len(documents))]
        self.vectore_store.add_documents(documents=documents, ids=uuids)

    def find_article_by_id(self, article_id: str):
        db_filter = {
            "must": [
                {"key": "metadata.article_id", "match": {"value": article_id}}
            ]
        }
        db_filter = Filter(**db_filter)
        result = self.client.scroll(
            collection_name=table_name,
            scroll_filter=db_filter,
            with_vectors=False,
            with_payload=True
        )[0]
        return bool(result)
    
qdrant_manager = QdrantManager()