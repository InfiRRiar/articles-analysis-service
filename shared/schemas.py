from pydantic import BaseModel

class SummarizationRequest(BaseModel):
    article: str
    mode: str

class AskRequest(BaseModel):
    article: str
    question: str

class AskResponse(BaseModel):
    answer: str


# LLM validate

class TermsOutput(BaseModel):
    terms: dict[str, str]

class UnifyTermsOutput(BaseModel):
    unique_terms: list[dict]

class TermsTypingOutput(BaseModel):
    terms: list[dict[str, str]]

class FindRelationsOutput(BaseModel):
    relations: list[dict[str, str]]

class TermsFromQueryOutput(BaseModel):
    terms: list[str]