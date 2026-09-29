from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.chatbot import Bot
from collections import defaultdict




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
    history: list[dict] = []


chatbot = Bot()

messages_counter = defaultdict(int)


@app.get("/")
def home():
    return {
        "message": "CV RAG chatbot is running"
    }


@app.get("/check/status")
def status():
    return {
        "status": "ok"
    }



@app.post("/chat")
def chat(request_ip: Request, request: ChatRequest):
    message_limit = 8
    client_ip = request_ip.client.host

    if messages_counter[client_ip] >= message_limit:
        return {"answer": "Unfortunately, you've reached the 8-question limit. To keep the chatbot free, no further questions are available. Thanks for chatting! 😊", "message_count": messages_counter[client_ip], 'message_limit': message_limit}
    else:
        results = chatbot.execute_bot(request.message, request.history)
        answer = results["answer"]
        sources = results["sources"] 
        # if messages_counter[client_ip] == 0:
        #     answer = "Good question!😄 " + answer
        if messages_counter[client_ip] == 2:
            answer = "Wow, you're really curious! 😄 Let's grab a coffee instead of chatting here ☕. Reach out to me at dennisgloukhman@hotmail.de\n\n Back to your question:   " + answer

           
    messages_counter[client_ip] += 1


    return {"answer": answer, "sources": sources, "message_count": messages_counter[client_ip], 'message_limit': message_limit  }


