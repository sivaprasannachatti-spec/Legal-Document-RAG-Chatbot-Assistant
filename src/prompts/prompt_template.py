import os
import sys
import json

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from src.utils import saveObject

@dataclass
class PromptTemplateConfig:
    rewrite_path = os.path.join("artifacts", "rewrite_prompt.json")
    query_path = os.path.join("artifacts", "query_prompt.json")
    title_path = os.path.join("artifacts", "title_prompt.json")

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
                ("system", """
You are an AI Legal Document Assistant specialized in analyzing legal contracts and policies.

Your job is to answer user questions ONLY using the provided legal context.

Follow these rules strictly:

CORE RULES:
1. Use ONLY the information provided in the context.
2. Do NOT hallucinate or create new legal rules.
3. If answer is not found in context, respond exactly:
   "Answer not found in provided context."
4. If answer exists, begin with:
   "According to the provided legal context,"
5. Be precise, professional, and legally accurate.
6. Keep answers concise and easy to understand.
7. Maintain polite and friendly tone.

CONVERSATION RULES:
- The conversation may contain follow-up questions.
- Always interpret the current question using conversation history if provided.
- If the question is unclear, answer based on best interpretation from context.

FORMAT RULES:
- Use short paragraphs.
- Use bullet points if multiple conditions/rules exist.
- Avoid long unnecessary explanations.
"""),
                ("system", "Legal Context:\n{context}"),
                (MessagesPlaceholder(variable_name='chat_history')),
                ("human", "{input}")
            ])
            title_prompt = ChatPromptTemplate([
                ('system', """
You are an helpful AI assistant. You create a approriate title for the first {message} sent by the user.
You assign and create an approriate title which is clear and descriptive. Below some
rules have been provided follow them as strictly as possible.

Rules:
1) Create an approriate title which is clear and descriptive based on the first message which user sends.
2) The title should have upto 3-5 words and not more than that.
3) No punctuation and No Quotes in title
4) Clear and descriptive

Title:""")
        ])
            rewrite_data = {"template": rewrite_prompt.messages[0].prompt.template}
            query_data = {"template": query_prompt.messages[0].prompt.template}
            title_data = {"template": title_prompt.messages[0].prompt.template}
            saveObject(path=self.templateConfig.rewrite_path, data=rewrite_data)
            saveObject(path=self.templateConfig.query_path, data=query_data)
            saveObject(path=self.templateConfig.title_path, data=title_data)
        except Exception as e:
            raise CustomException(e, sys)

if __name__=="__main__":
    template = PrompTemplate()
    template.createTemplate()