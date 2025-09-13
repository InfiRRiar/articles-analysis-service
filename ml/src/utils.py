from langchain_community.retrievers import ArxivRetriever
from langchain_core.documents.base import Document
import re

loader = ArxivRetriever(
    load_max_docs=1,
    get_full_documents=True,
    doc_content_chars_max=None
)

def clear_text(text: str):
    text = re.sub(r'-\n', "", text)
    text = re.sub(r'([^.])\n', r'\1 ', text)
    text = re.sub(r"\\n", "\n", text)
    
    print(len(text))

    return text

def load_document_from_web(article_id: str) -> Document:
    doc = loader.invoke(article_id)[0]

    doc.metadata = {"article_id": article_id}
    doc.page_content = clear_text(doc.page_content)
    return doc