from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.chatbot import Bot




app = FastAPI(
    title="CV RAG Chatbot",
    description="Chat with Dennis' CV using Gemini and RAG",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://dennisg.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


chatbot = Bot()



@app.get("/")
def home():
    return {
        "message": "CV RAG chatbot is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }



@app.post("/chat")
def chat(request: ChatRequest):
    answer = chatbot.execute_bot(request.message)
    return {"answer": answer}


