from pymongo import MongoClient
from os import getenv
from dotenv import load_dotenv
from bson import ObjectId

class Users:
    """
    User db model, creates new user
    METHODS: add_user
    """
    def __init__(self):
        self.connection = MongoClient(getenv("DB_CONNECTION_STRING"))
        self.users = self.connection.notesDb_api.users
        

    def add_user(self, doc:dict) -> dict:
        """
        REQUIRED FIELDS:Username, password
        """
        user = self.users
        try:
            inserted_user = user.insert_one(doc)
            if inserted_user.acknowledged:
                return {"id":f"{inserted_user.inserted_id}","message":"success"}
            else:
                return{"message":"insertion failed"}
        
        except Exception as error:
            return {"error":f"{error}"}


    def is_user(self, username:str):
        """Checks wheather the user is present in the database or not
            Returns : boolean : if user exists- True,else False
        """
        try:
            user = self.users
            user = user.find_one({"username":f"{username}"})
            if user:
                return True
            else:
                return False
        except Exception as error:
            return {"error":f"{error}"}
        
    def find_user(self, username:str):
        """
            find the user and return,
            parameter: username
        """
        try:
            user = self.users
            user = user.find_one({"username":f"{username}"})
            # if user present in return the user doc
            if user:
                return user
            else:
                return False
            
        except Exception as error:
            return {"error":f"{error}"}

        
