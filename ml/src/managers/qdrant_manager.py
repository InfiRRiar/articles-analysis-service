from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_core.documents import Document
from langchain_openai.embeddings import OpenAIEmbeddings
from loguru import logger
from uuid import uuid4
from qdrant_client.models import Filter


class QdrantManager():
    def __init__(self, table_name):
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
        self.table_name = table_name

    def add_articles(self, documents):
        uuids = [str(uuid4()) for _ in range(len(documents))]
        self.vectore_store.add_documents(documents=documents, ids=uuids)

    def find_documents_by_id(self, article_id: str) -> list[Document]:
        db_filter = {
            "must": [
                {"key": "metadata.article_id", "match": {"value": article_id}}
            ]
        }
        db_filter = Filter(**db_filter)
        article_docs = self.client.scroll(
            collection_name=self.table_name,
            scroll_filter=db_filter,
            with_vectors=False,
            with_payload=True
        )[0]

        return article_docs
    
    def search_relevant_chunks(
        self,
        query: str,
        article_id: str,
        k: int = 5,
    ) -> list[Document]:
        qdrant_filter = Filter(
            must=[
                {
                    "key": "metadata.article_id",
                    "match": {"value": article_id}
                }
            ]
        )
        docs = self.vectore_store.similarity_search(
            query=query,
            k=k,
            filter=qdrant_filter
        )

        return docs