from langchain_community.retrievers import ArxivRetriever
from langchain_core.documents.base import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


loader = ArxivRetriever(
    load_max_docs=1,
    get_full_documents=True
)

def load_document_from_web(article_id: str) -> Document:
    doc = loader.invoke(article_id)[0]
    return doc

class ArxivChunker:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=10)

    def get_documents(self, article_id: str) -> list[Document]:
        article_doc = load_document_from_web(article_id)
        text_fragments = self.text_splitter.split_text(article_doc.page_content)
        return text_fragments

    