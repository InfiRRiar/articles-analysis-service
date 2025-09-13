from src.managers.chunk_manager import ArxivChunker
from src.managers.mysql_manager import mysql_manager
from src.managers.qdrant_manager import qdrant_manager
from langchain_core.documents.base import Document
from src.utils import load_document_from_web

class Summarize:
    def __init__(self):
        self.qdrant_manager = qdrant_manager
        self.my_sql_manager = mysql_manager
        self.rag_chunker = ArxivChunker(500, 50)
        self.summarize_chunker = ArxivChunker(
            chunk_size=1000, 
            overlap=0
        )

    def invoke(self, article_id: str):
        article_text = self.my_sql_manager.find_article_by_id(article_id)
        if not article_text:
            article_doc = load_document_from_web(article_id)

            self.add_article_to_dbs(article_doc)
            article_text = article_doc.page_content

        resume = self.summarize(article_text)
        return article_text[:50]
    
    def add_article_to_dbs(self, article_doc: Document):
        rag_documents = self.rag_chunker.get_documents(article_doc)
        self.qdrant_manager.add_articles(rag_documents)

        self.my_sql_manager.add_article(article_doc)    
    
    def summarize(self, text: str) -> str:
        return text


summarize_pipeline = Summarize()