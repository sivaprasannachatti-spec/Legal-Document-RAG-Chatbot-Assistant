"""
Shared dependencies that are used across the backend.
This module exists to avoid circular imports — it holds objects
that would otherwise live in app.py but are needed by services.
"""
import os

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from src.utils import loadData
from src.components.data_retrieval import DataRetrieval

load_dotenv()

# load the vector db and splitted_docs
db = FAISS.load_local(
    "faiss_index",
    OllamaEmbeddings(model='nomic-embed-text:latest'),
    allow_dangerous_deserialization=True
)
docs = loadData(r'C:\Projects\artifacts\splitted_docs.pkl')

# pass the loaded vector db and docs into retrieval constructor
retrievalObj = DataRetrieval(vector_db=db, splitted_docs=docs)
