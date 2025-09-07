from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from shared.schemas import RequestData
import re
import requests

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
    data.article = extract_id(data.article)
    if not data.article:
        return {"summary": "Некорректная ссылка"}
    
    answer = requests.post("http://ml:8080/analyze", data=data.model_dump_json())
    
    return {"summary": answer.content}