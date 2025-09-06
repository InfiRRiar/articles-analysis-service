from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from shared.schemas import RequestData
import re

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")

def extract_id(line: str):    
    article_id = re.findall(r"[\d]+\.[\d]+", line)
    if not article_id:
        return None

    return article_id[0]

@app.get("/")
def main_page():
    return FileResponse("/web/src/templates/index.html")

@app.post("/analyze")
def analyze(data: RequestData):
    article_id = extract_id(data.article)
    if not article_id:
        return {"summary": "Некорректная ссылка"}
    
    return {"summary": article_id}