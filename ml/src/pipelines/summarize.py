from langchain_core.documents.base import Document
from langchain_core.output_parsers import StrOutputParser
from src.managers.chunk_manager import ArxivChunker
from src.managers.qdrant_manager import QdrantManager
from src.managers.mysql_manager import mysql_manager
from src.utils import load_document_from_web, create_chat
from langchain_openai import ChatOpenAI
from loguru import logger

class Summarize:
    def __init__(self):
        self.rag_qdrant_manager = QdrantManager("articles_rag")
        self.rag_chunker = ArxivChunker(500, 50)

        self.sum_chunker = ArxivChunker(1000, 0)
        self.sum_qdrant_manager = QdrantManager("articles_sum")

        self.my_sql_manager = mysql_manager

        self.chat = create_chat("summarize")
        
        self.model = ChatOpenAI(
            name="gpt-4.1-2025-04-14",
            base_url="https://api.proxyapi.ru/openai/v1"
        )
        self.sum_chain = self.chat | self.model | StrOutputParser()

    def invoke(self, article_id: str) -> str:
        logger.info("Invoke")
        docs_for_summarization = self.sum_qdrant_manager.find_documents_by_id(article_id)
        if not docs_for_summarization:
            article_doc = load_document_from_web(article_id)
            docs_for_summarization = self.add_article_to_dbs(article_doc)
        logger.info("Invoke 2")
        resume = self.summarize(docs_for_summarization)
        return resume
    
    def add_article_to_dbs(self, article_doc: Document) -> list[Document]:
        rag_documents = self.rag_chunker.split_documents(article_doc)
        self.rag_qdrant_manager.add_articles(rag_documents)

        sum_documents = self.sum_chunker.split_documents(article_doc)
        self.sum_qdrant_manager.add_articles(sum_documents)

        # self.my_sql_manager.add_article(article_doc)

        return sum_documents
    
    def summarize(self, docs: list[Document]) -> str:
        logger.info("Enter summarize")
        current_resume = ""
        for i, doc in enumerate(docs):
            logger.info(i)
            prompt_args = {
                "resume": current_resume,
                "text_chunk": doc.page_content,
            }
            current_resume = self.sum_chain.invoke(prompt_args)
        return current_resume

summarize_pipeline = Summarize()