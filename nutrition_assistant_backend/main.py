from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from agent import Agent

load_dotenv()

app = FastAPI()
agent = Agent()


class QueryRequest(BaseModel):
    user_input: str
    thread_id: str


@app.post("/ask")
def ask(request: QueryRequest):
    response = agent.handle(request.user_input, request.thread_id)
    return {"response": response}
