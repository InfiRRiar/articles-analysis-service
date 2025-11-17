from langchain_core.documents.base import Document
from langchain_core.output_parsers import StrOutputParser
from src.managers.chunk_manager import ArxivChunker
from src.managers.qdrant_manager import QdrantManager
from src.managers.mysql_manager import mysql_manager
from src.pipelines.make_onthology import onthology_maker
from src.utils import load_document_from_web, create_chat, clear_text
from src.main_components import model, rag_qdrant_manager
from loguru import logger

class Summarize:
    def __init__(self):
        self.rag_qdrant_manager = rag_qdrant_manager
        self.model = model
        self.onthology_maker = onthology_maker

        self.rag_chunker = ArxivChunker(500, 50)

        self.sum_chunker = ArxivChunker(3000, 0)
        self.sum_qdrant_manager = QdrantManager("articles_sum")

        self.my_sql_manager = mysql_manager

        self.sum_chat = create_chat("summarize")
        self.final_sum_chat = create_chat("final_summarization")

        self.sum_chain = self.sum_chat | self.model | StrOutputParser()
        self.final_sum_chain = self.final_sum_chat | self.model | StrOutputParser()

    def invoke(self, article_id: str) -> str:
        article_row = self.my_sql_manager.find_article_by_id(article_id)
        if not article_row or not len(article_row.summarization):
            article_doc = load_document_from_web(article_id)
            doc_texts = self._add_article_to_rel_db(article_doc)
            self._add_article_to_vector_db(article_doc)
            resume = self._summarize(doc_texts, article_id)
            self.my_sql_manager.add_summarization_to_article(article_id, resume)
            return resume
        
        article_sum = article_row.summarization

        doc = Document(article_sum)
        doc.metadata = {"article_id": article_id}

        self._add_article_to_vector_db(doc)
        return article_sum
    
    def _add_article_to_rel_db(self, article_doc: Document) -> list[Document]:
        sum_documents = self.sum_chunker.split_documents(article_doc)
        self.my_sql_manager.add_articles(sum_documents)

        # self.my_sql_manager.add_article(article_doc)

        return sum_documents
    
    def _add_article_to_vector_db(self, article_doc: Document):
        rag_documents = self.rag_chunker.split_documents(article_doc)
        self.rag_qdrant_manager.add_articles(rag_documents)
    
    def _summarize(self, docs: list[Document], article_id: str) -> str:
        logger.info("Enter summarize")
        resumes = []
        for i, doc in enumerate(docs):
            logger.info(str(i) + "/" + str(len(docs)))
            prompt_args = {
                "text_chunk": doc.page_content,
            }

            resume = self.sum_chain.invoke(prompt_args)
            resumes.append(resume)

        self.onthology_maker.invoke(article_id, resumes)

        all_resumes = {"text_chunk": "\n\n".join(resumes)}

        resume = self.final_sum_chain.invoke(all_resumes)
        
        return resume    


summarize_pipeline = Summarize() 