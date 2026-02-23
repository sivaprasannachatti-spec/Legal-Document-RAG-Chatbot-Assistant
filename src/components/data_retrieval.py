import os
import sys

from src.exception import CustomException
from src.logger import logging
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.retrievers import BM25Retriever, EnsembleRetriever
from langchain_core.prompts import load_prompt
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from src.utils import getImprovedQuery

class DataRetrieval:
    def __init__(self, vector_db, splitted_docs):
        try:
            logging.info("VectorDB retrieved successfully")
            self.semantic_retriever = vector_db.as_retriever()
            logging.info("Semantic retriever initialized successfully")
            self.bm25_retriever = BM25Retriever.from_documents(documents=splitted_docs)
            self.bm25_retriever.k = 5
            logging.info("BM25 retriever initialized successfully")
            logging.info("Combining the semantic and bm25 retrievers")
            self.hybrid_retriever = EnsembleRetriever(
                retrievers=[self.semantic_retriever, self.bm25_retriever],
                weights=[0.7, 0.3]
            )
            logging.info("Hybrid retriever initialized successfully")
        except Exception as e:
            raise CustomException(e, sys)
        
    def retrieveData(self, user_query):
        try:
            query_prompt = load_prompt(r'C:\Projects\artifacts\query_prompt.json')
            rewrite_prompt = load_prompt(r'C:\Projects\artifacts\rewrite_prompt.json')
            logging.info("Rewriting and Query prompts retrieved successfully")
            rewriting_model = ChatOllama(model='gemma3:270m')
            model = ChatOllama(model='tinyllama:1.1b')
            document_chain = create_stuff_documents_chain(llm=model, prompt=query_prompt)
            rewrite_chain = rewrite_prompt | rewriting_model | StrOutputParser()
            rewritten_query = getImprovedQuery(rewrite_chain, user_query)
            logging.info("Query rewritten successfully")
            retrieval_chain = create_retrieval_chain(self.hybrid_retriever, document_chain)
            logging.info("Retrieval chain initialized successfully")
            result = retrieval_chain.invoke({
                "input": user_query
            })
            return result['answer']
        except Exception as e:
            raise CustomException(e, sys)