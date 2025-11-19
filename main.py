from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.productivity_agent import ProductivityAgent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = ProductivityAgent()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    agent: str
    reply: str

@app.get("/")
def home():
    return {"message": "Backend running!"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    return agent.chat(req.message)
