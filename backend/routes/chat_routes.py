import sys

from fastapi import APIRouter, Response, Request, Depends
from backend.models.DB_Client import supabase
from src.exception import CustomException
from src.logger import logging
from backend.controllers.chat_controllers import getAllChats, getParticularChat, handleNewChatting, handleOldChatting
from backend.middlewares.auth_middlewares import verifyJWT
from pydantic import BaseModel, Field
from typing import Annotated

chat_router = APIRouter(dependencies=[Depends(verifyJWT)])

class User(BaseModel):
    message: Annotated[str, 'Message of the user', Field(..., description='Message of the user')]

@chat_router.get("/getAllChats")
def getChats(request: Request):
    try:
        return getAllChats(request=request)
    except Exception as e:
        raise CustomException(e, sys)
    
@chat_router.get("/getParticularChat/{chat_title}")
def getChat(chat_title):
    try:
        return getParticularChat(chat_title=chat_title)
    except Exception as e:
        raise CustomException(e, sys)

@chat_router.post("/newChat")
def createChat(user: User, request: Request):
    try:
        return handleNewChatting(user=user, request=request)
    except Exception as e:
        raise CustomException(e, sys)

@chat_router.post("/oldChat/{chat_title}")
def oldChat(chat_title, user: User):
    try:
        return handleOldChatting(title=chat_title, user=user)
    except Exception as e:
        raise CustomException(e, sys)