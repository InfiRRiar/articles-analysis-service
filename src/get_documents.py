from langchain_community.retrievers import ArxivRetriever
from langchain_core.documents.base import Document


loader = ArxivRetriever(
    load_max_docs=1,
    get_ful_document=True
)

# 2509.03558
def load_document_frow_web(article_id: str) -> Document:
    doc = loader.invoke(article_id)[0]
    return doc