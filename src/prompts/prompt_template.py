import os
import sys
import json

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from src.utils import saveObject

@dataclass
class PromptTemplateConfig:
    rewrite_path = os.path.join("artifacts", "rewrite_prompt.json")
    query_path = os.path.join("artifacts", "query_prompt.json")

class PrompTemplate:
    def __init__(self):
        self.templateConfig = PromptTemplateConfig()
    
    def createTemplate(self):
        try:
            os.makedirs(os.path.dirname(self.templateConfig.rewrite_path) ,exist_ok=True)
            rewrite_prompt = ChatPromptTemplate([
                ('system', """
You are an helpful AI legal document assistant. You help the users in rewriting their query whenever user passes a query to you.

Rewrite the user's question into a clear and complete legal query with proper punctuation and with right grammatical patterns
that will help the retrieve relevant contract clause.

Do not answer the question. Only rewrite it

Follow the guidelines as mentioned below as it is don't miss any guideline
Guidelines:
1) Rewrite the user's question into a clear and complete legal query with proper punctuation and with right grammatical patterns.
2) Do not answer the question
3) Only rewrite the query
4) 

User question:
{input}

Rewritten query:
""")
        ])
            query_prompt = ChatPromptTemplate([
                ('system', """
You are an helpful AI legal document assistant. You help the users in resolving their queries. Your main task is to resolve the user query
from the provided context from legal contracts. You answer from the provided context don't hallucinate yourself and don't make up of new rules.

Below some guidelines are provided follow them as strictly as possible. Guidelines goes as follows:
Guidelines:
1) Use only provided context
2) Do not make up information and don't hallucinate
3) If the answer is not present in the context, say: "Answer not found in provided context"
4) If the answer is present in the context, then say according to the context.
4) Be precise and professional
5) Be friendly with user don't answer the user in a rude way. Be polite and professional

Context:
{context}

Question:
{input}

AI:""")
        ])
            rewrite_data = {"template": rewrite_prompt.messages[0].prompt.template}
            query_data = {"template": query_prompt.messages[0].prompt.template}
            saveObject(path=self.templateConfig.rewrite_path, data=rewrite_data)
            saveObject(path=self.templateConfig.query_path, data=query_data)
        except Exception as e:
            raise CustomException(e, sys)

if __name__=="__main__":
    template = PrompTemplate()
    template.createTemplate()