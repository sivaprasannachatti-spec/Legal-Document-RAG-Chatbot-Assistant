import pickle

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.data_retrieval import DataRetrieval
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from src.utils import saveObject

if __name__=="__main__":
    ingestionObj = DataIngestion()
    print("In Ingestion")
    docs = ingestionObj.loadData()
    transformationObj = DataTransformation()
    print("In Transformation")
    splitted_docs = transformationObj.transformData(docs)
    db = FAISS.load_local(
        "faiss_index",
        OllamaEmbeddings(model='nomic-embed-text:latest'),
        allow_dangerous_deserialization=True   
    )
    print("In Retrieval")
    retrievalObj = DataRetrieval(vector_db=db, splitted_docs=splitted_docs)
    print(retrievalObj.retrieveData(user_query="Late Penalty?"))

