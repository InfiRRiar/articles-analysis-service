from fastapi import FastAPI
from shared.schemas import RequestData
from ml.src.pipelines.summarize import summarize_pipeline

app = FastAPI()

@app.post("/analyze")
def analyze(data: RequestData):
    result = summarize_pipeline.invoke(data.article)
    return result
    