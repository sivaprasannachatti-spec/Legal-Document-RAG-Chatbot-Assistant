from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.routes.user_routes import user_router
from backend.routes.chat_routes import chat_router
from src.components.data_retrieval import DataRetrieval
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from src.utils import loadData
import os

app = FastAPI()

# Allow requests from any origin (Swagger docs, frontend, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = FAISS.load_local(
        "faiss_index",
        OllamaEmbeddings(model='nomic-embed-text:latest'),
        allow_dangerous_deserialization=True   
    )
docs = loadData(r'C:\Projects\artifacts\splitted_docs.pkl')

retrievalObj =DataRetrieval()

app.include_router(user_router, prefix="/api/user")
app.include_router(chat_router, prefix="/api/chat")

# Serve frontend
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

# Static assets (css, js)
app.mount("/css", StaticFiles(directory=os.path.join(FRONTEND_DIR, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(FRONTEND_DIR, "js")), name="js")

# SPA routes — all serve index.html, JS handles routing
@app.get("/")
async def serve_root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"), headers={"Cache-Control": "no-cache"})

@app.get("/login")
async def serve_login():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"), headers={"Cache-Control": "no-cache"})

@app.get("/signup")
async def serve_signup():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"), headers={"Cache-Control": "no-cache"})

@app.get("/chat")
async def serve_chat():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"), headers={"Cache-Control": "no-cache"})
