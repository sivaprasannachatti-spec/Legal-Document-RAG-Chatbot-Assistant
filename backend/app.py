import os

from fastapi import FastAPI
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from src.utils import loadData
from src.components.data_retrieval import DataRetrieval
from backend.routes.user_routes import user_router
from backend.routes.chat_routes import chat_router

load_dotenv()

app = FastAPI()

# load the vector db and splitted_docs
db = FAISS.load_local(
        "faiss_index",
        OllamaEmbeddings(model='nomic-embed-text:latest'),
        allow_dangerous_deserialization=True   
    )
docs = loadData(r'C:\Projects\artifacts\splitted_docs.pkl')

# pass the loaded vector db and docs into retrieval constructor
retrievalObj = DataRetrieval(vector_db=db, splitted_docs=docs)

app.include_router(user_router, prefix="/api/user")
app.include_router(chat_router, prefix="/api/chat")

