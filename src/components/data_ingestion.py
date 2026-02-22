import os
import sys

from src.exception import CustomException
from src.logger import logging
from langchain_classic.document_loaders import DirectoryLoader, TextLoader
from src.components.data_transformation import DataTransformation
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from src.components.data_retrieval import DataRetrieval

class DataIngestion:
    def loadData(self):
        try:
            loader = DirectoryLoader(
            path=r'C:\Projects\contracts',
            glob='**/*.txt',
            loader_cls = TextLoader,
            loader_kwargs={'encoding': 'utf-8'}
            )
            logging.info("Loader initialized successfully")
            docs = loader.load()
            logging.info("All documents loaded successfully")
            return docs
        except Exception as e:
            raise CustomException(e, sys)
