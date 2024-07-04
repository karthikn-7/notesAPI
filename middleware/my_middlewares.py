from flask import jsonify, request
import jwt
from os import getenv
from dotenv import load_dotenv
from functools import wraps
load_dotenv('../.env')



def tokenvalidator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            token = request.headers.get("Authorization")
            
            if not token:
                return jsonify({"message":"Token is missing!"}),401
            else:
                token = token.split(" ")[1]
                jwt.decode(token,key=getenv("JWT_SECRET_KEY"),algorithms=getenv("ALGORITHM"))
                return func(*args, **kwargs)
        
        except jwt.ExpiredSignatureError :
            return jsonify({"message":"Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message":"Invalid Token!"}), 401
        
    return wrapper
