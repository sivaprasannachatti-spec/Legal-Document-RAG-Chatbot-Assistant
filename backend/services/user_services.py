import sys

from src.exception import CustomException
from src.logger import logging
from backend.models.DB_Client import supabase
from fastapi.responses import JSONResponse

def insertData(user):
    try:
        response = (
            supabase.table("users")
            .select("email")
            .eq("email", user.email)
            .execute()
        )
        if(response.data):
            return JSONResponse(status_code=400, content={"message": "User already exists"})
        (
            supabase.table("users")
            .insert({
                "name": user.name,
                "email": user.email,
            })
            .execute()
        )
        return JSONResponse(status_code=201, content={"message": "User inserted successfully"})
    except Exception as e:
        raise CustomException(e, sys)
