from langchain_core.output_parsers import PydanticOutputParser
from src.main_components import model
from src.utils import create_chat
from src.managers.mysql_manager import mysql_manager
from shared.schemas import TermsOutput, UnifyTermsOutput, TermsTypingOutput, FindRelationsOutput
from loguru import logger

class OnthologyMaker:
    def __init__(self):
        self.model = model
        self.mysql_manager = mysql_manager

        self.fetch_terms_chat = create_chat("fetch_terms")
        self.remove_doubles_chat = create_chat("remove_doubles")
        self.terms_typing_chat = create_chat("terms_typing")
        self.find_relations_chat = create_chat("find_relations")
        
        self.fetch_terms_chain = self.fetch_terms_chat | self.model | PydanticOutputParser(pydantic_object=TermsOutput)
        self.remove_doubles_chain = self.remove_doubles_chat | self.model | PydanticOutputParser(pydantic_object=UnifyTermsOutput)
        self.terms_typing_chain = self.terms_typing_chat | self.model | PydanticOutputParser(pydantic_object=TermsTypingOutput)
        self.find_relations_chain = self.find_relations_chat | self.model | PydanticOutputParser(pydantic_object=FindRelationsOutput)

    def invoke(self, article_id: str, chunks: list[str]) -> dict[str, str]:
        terms = self._get_terms(chunks)

        typed_terms = self.terms_typing_chain.invoke({"terms_with_definitions": terms}).terms

        onthology = self._establish_relations(typed_terms)
        
        self.mysql_manager.add_onthology_to_article(article_id, onthology)
        self.mysql_manager.add_terms_to_article(article_id, terms)
            
    def _get_terms(self, chunks) -> dict[str, list[str]]:
        ejected_terms = {}
        for chunk in chunks:
            output = self.fetch_terms_chain.invoke({"input_text": chunk})
            for key, val in output.terms.items():
                if key not in ejected_terms:
                    ejected_terms[key] = []
                ejected_terms[key] += [val]
        united_terms = self.remove_doubles_chain.invoke({"terms_dict": ejected_terms}).unique_terms

        logger.info(united_terms)

        for term in united_terms:
            term["definition"] = ""
            for i in range(len(term["merged"])):
                if term["merged"][i] in ejected_terms:
                    term["definition"] = ejected_terms[term["merged"][i]]
                    break
            term.pop("merged")

        return united_terms

    def _establish_relations(self, terms):
        result = self.find_relations_chain.invoke({"terms_with_definitions_and_types": terms})

        return result.relations

onthology_maker = OnthologyMaker()