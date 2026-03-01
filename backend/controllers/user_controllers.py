import sys
import os
import datetime

from src.exception import CustomException
from src.logger import logging
from backend.models.DB_Client import supabase
from backend.services.user_services import insertData
from jose import jwt
from fastapi.responses import JSONResponse
from fastapi import HTTPException

def handleSignupUser(user):
    try:
        return insertData(user=user)
    except Exception as e:
        raise CustomException(e, sys)

def createToken(payload, key, algorithm):
    try:
        token = jwt.encode(payload, key, algorithm=algorithm)
        return token
    except Exception as e:
        raise CustomException(e, sys)

def handleLoginUser(user, response):
    try:
        key = os.environ["JWT_SECRET_KEY"]
        algorithm = "HS256"
        db_response = (
            supabase.table("users")
            .select("user_id, email")
            .eq("email", user.email)
            .execute()
        )

        if not db_response.data:
            return JSONResponse(status_code=400, content={"message": "User not found. Please signup first"})
        
        user = db_response.data[0]
        #create a payload data
        payload = {
            "user_id": user["user_id"],
            "email": user["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=36500)
        }
        token = createToken(payload=payload, key=key, algorithm=algorithm)
        # Set the cookie on the SAME response object we return
        json_response = JSONResponse(status_code=200, content={"message": "User logged in successfully", "email": user["email"]})
        json_response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            max_age=30 * 24 * 60 * 60,  # 30 days in seconds
            samesite="lax"
        )
        return json_response
    except Exception as e:
        raise CustomException(e, sys)

def handleLogoutUser(request, response):
    try:
        # Only clear the cookie — do NOT delete the user from the database
        json_response = JSONResponse(status_code=200, content={"message": "User logged out successfully"})
        json_response.delete_cookie(key="access_token")
        return json_response
    except Exception as e:
        raise CustomException(e, sys)
    
def getUserDetails(email):
    try:
        if not email:
            raise HTTPException(status_code=422, detail='Please provide valid email')
        # get the user by matching the user's email
        response = (
            supabase.table("users")
            .select("*")
            .eq("email", email)
            .execute()
        )
        if not response.data:
            raise HTTPException(status_code=404, detail='User not found with specified email')
        return JSONResponse(status_code=200, content={"message": "User details fetched successfully", "data": response.data[0]})
    except Exception as e:
        raise CustomException(e, sys)