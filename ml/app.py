from fastapi import FastAPI
from shared.schemas import SummarizationRequest, AskResponse, AskRequest
from src.pipelines.summarize import summarize_pipeline
from src.pipelines.prepare_answers import answer_pipeline

app = FastAPI()

@app.post("/analyze")
def analyze(data: SummarizationRequest):
    result = summarize_pipeline.invoke(data.article)
    return result

@app.post("/ask")
def prepare_answer(data: AskRequest):
    result = answer_pipeline.invoke(question=data.question, article_id=data.article)
    return result