from fastapi import FastAPI
from shared.schemas import RequestData
from src.pipelines.analyze import analyze_pipeline

app = FastAPI()

@app.post("/analyze")
def analyze(data: RequestData):
    result = analyze_pipeline.invoke(data.article)
    return result
    