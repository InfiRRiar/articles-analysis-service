from pydantic import BaseModel

class RequestData(BaseModel):
    article: str
    mode: str