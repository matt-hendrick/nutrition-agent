import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import Agent

load_dotenv()

app = FastAPI()
agent = Agent()

IS_PRODUCTION = os.getenv("RAILWAY_ENVIRONMENT") == "production"

# Production-only CORS configuration for Railway
if IS_PRODUCTION:
    FRONTEND_DOMAIN = os.getenv("FRONTEND_DOMAIN")

    if not FRONTEND_DOMAIN:
        raise ValueError(
            "FRONTEND_DOMAIN environment variable must be set in production"
        )

    CORS_ORIGINS = [FRONTEND_DOMAIN]

else:
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    user_input: str
    thread_id: str


@app.post("/ask")
def ask(request: QueryRequest):
    response = agent.handle(request.user_input, request.thread_id)
    return {"response": response}
