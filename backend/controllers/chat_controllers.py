import sys

from src.exception import CustomException
from src.logger import logging
from backend.models.DB_Client import supabase
from fastapi import HTTPException, JSONResponse
from backend.services.chat_services import getChats, getChat, performChatting
from langchain_core.prompts import load_prompt
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

def getAllChats(request):
    try:
        id = request.state.user['user_id']
        if not id:
            raise HTTPException(status_code=404, detail='The specified user is not found')
        response = (
            supabase.table("chats")
            .select("chat_id")
            .eq("user_id", id)
            .execute()
        )
        if not response.data:
            raise HTTPException(status_code=404, detail='No chats found')
        chats = getChats(response.data)
        if not chats:
            raise HTTPException(status_code=500, detail='Something went wrong while retrieving the chats')
        return JSONResponse(status_code=200, content={"message": "All chats retrieved successfully", "chats": chats})
    except Exception as e:
        raise CustomException(e, sys)

def getParticularChat(chat_title: str):
    try:
        if not chat_title:
            raise HTTPException(status_code=400, detail='Valid title is required')
        response = (
            supabase.table("chats")
            .select("chat_id")
            .eq("chat_title", chat_title)
            .execute()
        )
        if not response.data:
            raise HTTPException(status_code=404, detail='The specified chat is not found')
        
        chat = getChat(response.data[0])
        if not chat:
            raise HTTPException(status_code=500, detail='Something went wrong while retrieving the specified chat')
        return JSONResponse(status_code=200, content={'message': "Specified chat retrieved successfully", "chat": chat})
    except Exception as e:
        raise CustomException(e, sys)

def handleNewChatting(user, request):
    try:
        if not user.message:
            raise HTTPException(status_code=400, detail='Please provide a valid message')
        prompt = load_prompt(r'C:\Projects\artifacts\title_prompt.json')
        model = ChatOllama(model='qwen2.5:3b')
        chain = prompt | model | StrOutputParser()
        result = chain.invoke({"message": user.message})
        result = StrOutputParser().parse(result)
        response = (
            supabase.table("chats")
            .insert({"user_id": request.state.user['user_id'], "chat_title": result})
            .execute()
        )
        response = performChatting(user.message, response.data[0]['chat_id'], [])
        return JSONResponse(status_code=201, content={
            "message": "Response received successfully", 
            "user_message":user.message, 
            "response": response}
            )
    except Exception as e:
        raise CustomException(e, sys)

def handleOldChatting(title, user):
    try:
        if not title:
            raise HTTPException(status_code=400, detail='Please provide a valid title')
        response = (
            supabase.table("chats")
            .select("chat_id")
            .eq("chat_title", title)
            .execute()
        )
        if not response.data:
            raise HTTPException(status_code=404, detail='Chat not found')
        chat_id = response.data[0]['chat_id']
        chat = getChat(chat_id=response.data[0])
        if not chat:
            raise HTTPException(status_code=500, detail='Something went wrong while retrieving the chat')
        llm_response = performChatting(msg=user.message, chat_id=chat_id, history=chat)
        if not llm_response:
            raise HTTPException(status_code=501, detail='Something went wrong while returning the response')
        return JSONResponse(status_code=201, content={
            "message": "Chat continued successfully", 
            "user_message": user.message,
            "LLM_response": llm_response
            }
        )
    except Exception as e:
        raise CustomException(e, sys)