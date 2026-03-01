import sys

from src.exception import CustomException
from src.logger import logging
from backend.models.DB_Client import supabase
from fastapi import HTTPException
from backend.dependencies import retrievalObj

def getChats(chat_ids):
    try:
        chats = {}
        for chat in chat_ids:
            chat_id = chat.get("chat_id")
            chat_title = chat.get("chat_title", chat_id)
            response = (
                supabase.table("messages")
                .select("role, content")
                .eq("chat_id", chat_id)
                .order("created_at", desc=False)
                .execute()
            )
            if response.data:
                chats[chat_title] = response.data
        return chats
    except Exception as e:
        raise CustomException(e, sys)

def getChat(chat_id):
    try:
        chats = {}
        response = (
            supabase.table("messages")
            .select("role, content")
            .eq("chat_id", chat_id['chat_id'])
            .execute()
        )
        if not response.data:
            raise HTTPException(status_code=404, detail='The specified chat did not retrieve successfully')
        chats['chat_id'] = response.data
        return chats
    except Exception as e:
        raise CustomException(e, sys)

def performChatting(msg, chat_id, history):
    try:
        if not msg:
            raise HTTPException(status_code=400, detail='Please provide a valid message')
        response = retrievalObj.retrieveData(user_query=msg, chat_history=history)
        if not response:
            raise HTTPException(status_code=500, detail='Something went wrong which producing the response')
        (
            supabase.table("messages")
            .insert([
                {"chat_id": chat_id, "role": "user", "content": msg},
                {"chat_id": chat_id, "role": "LLM", "content": response}
            ])
            .execute()
        )
        return response
    except Exception as e:
        raise CustomException(e, sys)