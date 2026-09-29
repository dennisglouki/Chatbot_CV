## Overview

This RAG chatbot was developed as a simple portfolio demonstration of an **end-to-end AI application**, combining a React frontend, FastAPI backend, vector search, and LLM-based response generation.
**Live application:** [https://dennisg.onrender.com/](https://dennisg.onrender.com/?utm_source=chatgpt.com)

The chatbot allows recruiters to explore my CV in more depth, learn about my projects, and ask questions about my previous research. 
The application will be continuously improved and extended.

### RAG Pipeline

User queries are embedded using the **Gemini API**. Semantic similarity search is performed using a **FAISS vector index** containing chunks from my CV and research documents.
The most relevant chunks are retrieved and passed as context to **Gemini 3.8 Flash** as the LLM, which generates a response based on the underlying documents.

### Backend

The backend is a **FastAPI** service handling chat requests, conversation history, and API communication. The backend and RAG pipeline were developed by me.
Responses are generated using the actual content of my CV and research papers rather than relying solely on general model knowledge.

### Frontend

The frontend is a **React/Vite** application providing the portfolio interface and interactive CV chatbot.
The frontend was adapted from the open-source [AlonXt/ai-portfolio](https://github.com/AlonXt/ai-portfolio) project.

### Deployment
The frontend and backend are deployed separately on **Render's free tier**. 
The frontend communicates with the FastAPI backend.


