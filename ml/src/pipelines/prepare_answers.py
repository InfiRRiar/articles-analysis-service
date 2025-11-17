from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from loguru import logger
from src.main_components import model, rag_qdrant_manager
from src.utils import create_chat
from src.managers.mysql_manager import mysql_manager
from shared.schemas import TermsFromQueryOutput
import json

class AnswerTheQuestion:
    def __init__(self):
        self.qa_chat = create_chat("answer_the_question")
        self.find_terms_chat = create_chat("fetch_terms_from_query")

        self.answer_chain = self.qa_chat | model | StrOutputParser()
        self.find_terms_chain = self.find_terms_chat | model | PydanticOutputParser(pydantic_object=TermsFromQueryOutput)

        self.qdrant_manager = rag_qdrant_manager
        self.mysql_manager = mysql_manager

    def invoke(self, question: str, article_id) -> str:
        primary_terms = set(self.eject_onthology_terms(question, article_id))

        logger.info("eject terms from query")
        logger.info(primary_terms)
        
        onthology = self.mysql_manager.find_article_by_id(article_id).onthology
        onthology = json.loads(onthology)["onthology"]

        secondary_terms_to_search = set()
        for relation in onthology:
            for term in primary_terms:
                if term in [relation["from"], relation["to"]]:
                    secondary_terms_to_search.add(relation["from"])
                    secondary_terms_to_search.add(relation["to"])

        secondary_terms_to_search -= primary_terms

        logger.info("second terms to search")
        logger.info(secondary_terms_to_search)

        all_fragments = set()
        all_fragments = all_fragments.union(set(self.qdrant_manager.search_relevant_chunks(question, article_id, k=5)))
        for f_term in primary_terms:
            all_fragments = all_fragments.union(self.qdrant_manager.search_relevant_chunks(f_term, article_id, k=2))
        
        for s_term in secondary_terms_to_search:
            all_fragments = all_fragments.union(self.qdrant_manager.search_relevant_chunks(s_term, article_id, k=1))

        docs = [doc.page_content for doc in list(all_fragments)]
        logger.info(docs)
        args = {
            "context": "\n\n".join(docs),
            "question": question
        }
        response = self.answer_chain.invoke(args)

        return response
     
    def eject_onthology_terms(self, query: str, article_id: str):
        terms = self.mysql_manager.find_article_by_id(article_id).terms
        logger.info(terms)
        terms = [i["canonical"] for i in terms]

        ejected_terms = self.find_terms_chain.invoke(
            input={
                "terms": terms,
                "question": query
            }
        )
        return ejected_terms.terms

answer_pipeline = AnswerTheQuestion()  