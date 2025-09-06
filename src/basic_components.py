from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_openai.embeddings import OpenAIEmbeddings
import os

API_KEY = os.getenv("API_KEY")

class BasicComponents():
    def __init__(self):
        self.client: QdrantClient = QdrantClient(":memory:")
        self.client.create_collection(
            collection_name="articles",
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )

        self.vectore_store: QdrantVectorStore = QdrantVectorStore(
            client=self.client,
            collection_name="articles_pages"
        )

        self.embedder: OpenAIEmbeddings = OpenAIEmbeddings(
            model = "text-embedding-3-small",
            dimensions=1536,
            base_url="https://api.proxyapi.ru/openai/v1",
            api_key=API_KEY
        )
    def add_document(self):
        pass

    def find(self):
        pass

basic_components = BasicComponents()