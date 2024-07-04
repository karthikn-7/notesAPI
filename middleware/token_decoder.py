import jwt
from os import getenv
from flask import request

def decodeToken():
    """
    Return the payload of the token
    """
    try:
        token = request.headers.get("Authorization")
        token = token.split(" ")[1]
        data = jwt.decode(token,getenv("JWT_SECRET_KEY"),algorithms=getenv("ALGORITHM"))
        return data
    except Exception as error:
        return error