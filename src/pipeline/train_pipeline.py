import pickle

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.data_retrieval import DataRetrieval
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from src.utils import saveObject
from src.evaluation.data_preparation import DataPreparation

if __name__=="__main__":
    ingestionObj = DataIngestion()
    print("In Ingestion")
    docs = ingestionObj.loadData()
    transformationObj = DataTransformation()
    print("In Transformation")
    splitted_docs, db = transformationObj.transformData(docs)
    print("In Retrieval")
    evaluation_obj = DataPreparation()
    print("In evaluation")
    print(evaluation_obj.prepareData(docs=splitted_docs))
    # retrievalObj = DataRetrieval(vector_db=db, splitted_docs=splitted_docs)
    # print(retrievalObj.retrieveData(user_query="Late Penalty?", chat_history=[]))

