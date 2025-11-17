from langchain_community.retrievers import ArxivRetriever
from langchain_core.documents.base import Document
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage
import re
from loguru import logger


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

def create_chat(name: str):
    with open(f"/ml/src/prompts/{name}-system.txt", encoding="utf-8") as f:
        system_message = f.read()
    with open(f"/ml/src/prompts/{name}-user.txt", encoding="utf-8") as f:
        user_message = f.read()

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            ("user", user_message),
        ]
    ) 
    return prompt_template