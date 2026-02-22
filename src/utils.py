import os
import sys
import re
import json

from src.exception import CustomException
from src.logger import logging
from langchain_core.documents import Document
from langchain_ollama import ChatOllama

def split_into_sections(text):
    """
    Try to split document into sections using flexible patterns.
    If no sections found, returns full text as single section.
    """

    # flexible heading detection
    pattern = r'\n(?=(SECTION|Section|ARTICLE|Article|[A-Z][A-Z\s]{4,}|[0-9]+\.[0-9]+|[0-9]+\.)\s)'

    parts = re.split(pattern, text)

    sections = []
    buffer = ""

    for part in parts:
        if part is None:
            continue

        # detect heading-like text
        if re.match(r'(SECTION|Section|ARTICLE|Article)', part) or \
           re.match(r'[A-Z][A-Z\s]{4,}', part) or \
           re.match(r'[0-9]+\.', part):

            if buffer.strip():
                sections.append(buffer.strip())
            buffer = part
        else:
            buffer += part

    if buffer.strip():
        sections.append(buffer.strip())

    # if no real sections found → return full doc
    if len(sections) <= 1:
        return [text]

    return sections

def getFinalChunks(docs):
    final_chunks = []
    for doc in docs:
        section = split_into_sections(doc.page_content)
        for sec in section:
            final_chunks.append(
                Document(
                    page_content=sec,
                    metadata=doc.metadata
                )
            )
    return final_chunks

def saveObject(path, data):
    try:
        with open(path, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        raise CustomException(e, sys)

def getImprovedQuery(chain, query):
    try:
        logging.info("Model initialized successfully")
        rewritten_query = chain.invoke({
            "input": query
        })
        return rewritten_query
    except Exception as e:
        raise CustomException(e, sys)