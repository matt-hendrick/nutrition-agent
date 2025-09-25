from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import Agent

load_dotenv()

app = FastAPI()
agent = Agent()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    user_input: str
    thread_id: str


@app.post("/ask")
def ask(request: QueryRequest):
    response = agent.handle(request.user_input, request.thread_id)
    return {"response": response}
