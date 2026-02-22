import os
import sys

from src.exception import CustomException
from src.logger import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS  
from src.utils import getFinalChunks
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv

load_dotenv()

class DataTransformation:
    def transformData(self, docs: list):
        try:
            logging.info("Data loaded successfully")
            final_chunks = getFinalChunks(docs)
            logging.info("Final chunks retrieved successfully")
            logging.info("Getting the splitted docs by sending the final chunks as parameter to the text splitter")
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=500,
                separators=[
                    "\n\n",
                    "\n",
                    ". "
                ]
            )
            logging.info("Splitter initialized successfully")
            splitted_docs = splitter.split_documents(final_chunks)
            logging.info("Final splitted documents retrieved successfully")
            embedding_model = OllamaEmbeddings(model='nomic-embed-text:latest')
            logging.info("Embedding model initialized successfully")
            vector_db = FAISS.from_documents(documents=splitted_docs, embedding=embedding_model)
            logging.info("Splitted documents stored successfully")
            vector_db.save_local("faiss_index")   
            return splitted_docs
        except Exception as e:
            raise CustomException(e, sys)

        