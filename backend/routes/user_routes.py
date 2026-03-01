import sys

from fastapi import APIRouter, Response, Request, Depends
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated
from src.exception import CustomException
from backend.controllers.user_controllers import handleSignupUser, handleLoginUser, handleLogoutUser, getUserDetails
from backend.models.DB_Client import supabase
from backend.middlewares.auth_middlewares import verifyJWT

user_router = APIRouter()

class Signup(BaseModel):
    name: Annotated[str, Field(..., description='Name of the user', max_length=50)]
    email: Annotated[EmailStr, Field(..., description='Email of the user', max_length=100)]

class Login(BaseModel):
    email: Annotated[EmailStr, Field(..., description='Email of the user', max_length=100)]

@user_router.post("/signup")
def signup(user: Signup):
    try:
        return handleSignupUser(user=user)
    except Exception as e:
        raise CustomException(e, sys)

@user_router.post("/login")
def login(user: Login, response: Response):
    try:
        return handleLoginUser(user=user, response=response)
    except Exception as e:
        raise CustomException(e, sys)

@user_router.delete("/logout", dependencies=[Depends(verifyJWT)])
def logout(request: Request, response: Response):
    try:
        return handleLogoutUser(request=request, response=response)
    except Exception as e:
        raise CustomException(e, sys)

@user_router.get("/details/{email}", dependencies=[Depends(verifyJWT)])
def getUser(email: str):
    try:
        return getUserDetails(email=email)
    except Exception as e:
        raise CustomException(e, sys)

@user_router.get("/me", dependencies=[Depends(verifyJWT)])
def checkSession(request: Request):
    """Check if the user's JWT cookie is still valid. Returns user info."""
    try:
        user = request.state.user
        return {"authenticated": True, "email": user["email"]}
    except Exception as e:
        raise CustomException(e, sys)