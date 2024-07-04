from pymongo import MongoClient
from os import getenv
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv("../.env")
db_string = getenv("DB_CONNECTION_STRING")
class Notes:
    # initialization
    def __init__(self):
        self.connection = MongoClient(db_string)
        self.notesdb = self.connection.notesDb_api
        self.notesdbcoll = self.notesdb.notes

    # check connections
    def check_connection(self):
        conn = self.connection
        if conn:
            return f"DB Connected successfully!, Host:{conn.HOST}, Address:{conn.address}"
        else:
            return "Error connecting db"
    
    # show all databases
    def show_dbs(self):
        conn = self.connection
        return conn.list_database_names()
    
    # create note
    def create_note(self, note_doc:dict):
        try:
            notescoll = self.notesdbcoll
            created_coll = notescoll.insert_one(document=note_doc)
            aknowledgement = {
                "created" : created_coll.acknowledged,
                "id": created_coll.inserted_id
            }
            return aknowledgement
        except Exception as error:
            return f"Error Inserting document: {error}"
    
    # show all notes
    def get_all_notes(self, userid):
        try:
            notescoll = self.notesdbcoll
            notes = list(notescoll.find({"userid":f"{userid}",},{"userid":False}))
            return notes
            
        except Exception as ex:
            return ex
        
    # get notes by id
    def get_note_by_id(self, id:str):
        try:
            notescoll = self.notesdbcoll
            id = ObjectId(id)
            note = notescoll.find_one({"_id":id}, {"userid":False})
            return note
        except Exception as error:
            return f"Error getting document: {error}"
    
    # delete by oid
    def delete_note(self, id:str):
        try:
            notescoll = self.notesdbcoll
            id = ObjectId(id)
            deleted_note = notescoll.delete_one({"_id":id})
            return deleted_note.acknowledged

        except Exception as error:
            return f"Error deleting document: {error}"
    
    # find note by id
    def find_note(self, id:str):
        try:
            notescoll = self.notesdbcoll
            id = ObjectId(id)
            note = notescoll.find_one({"_id":id})
            return note

        except Exception as error:
            return f"Error finding document: {error}"
        
    # update note
    def update_by_id(self, id:str, note_doc:dict):
        try:
            notescoll = self.notesdbcoll
            id = ObjectId(id)
            note = notescoll.find_one_and_update({ "_id":id }, {"$set":note_doc} )
            return note
        
        except Exception as error:
            return error

