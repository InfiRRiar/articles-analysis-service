from langchain_core.documents.base import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

class ArxivChunker:
    def __init__(self, chunk_size: int, overlap: int):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)

    def get_documents(self, doc: Document) -> list[Document]:
        docs = self.text_splitter.split_documents([doc])
        return docs