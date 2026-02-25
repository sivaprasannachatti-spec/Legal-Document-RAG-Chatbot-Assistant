import sys
import os

from jose import jwt
from fastapi import Request, HTTPException
from src.exception import CustomException
from src.logger import logging
from backend.models.DB_Client import supabase

async def verifyJWT(request: Request):
    try:
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail='Token not found. Please Login first')
        decodedToken = jwt.decode(token=token, key=os.environ["JWT_SECRET_KEY"], algorithms="HS256")
        response = (
            supabase.table("users")
            .select("user_id, email")
            .eq("user_id", decodedToken["user_id"])
            .execute()
        )
        if not response.data:
            raise HTTPException(status_code=400, detail='User not found')
        request.state.user = response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise CustomException(e, sys)