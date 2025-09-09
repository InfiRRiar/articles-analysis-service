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
    def __init__(self, chunk_size: int, overlap: int):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)

    def get_documents(self, article_id: str) -> list[Document]:
        article_doc = load_document_from_web(article_id)
        article_doc.metadata = {"article_id": article_id}

        docs = self.text_splitter.split_documents([article_doc])
        return docs