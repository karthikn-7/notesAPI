import datetime
from models.notes_model import Notes
from models.users_model import Users
from flask import jsonify, request, json
from bson import ObjectId, json_util
from flask import Flask, render_template
from flask_cors import CORS
import jwt
from dotenv import load_dotenv
from os import getenv
from datetime import timedelta 
import datetime
from middleware.my_middlewares import tokenvalidator
import bcrypt
from middleware.token_decoder import decodeToken 


load_dotenv()
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = getenv("JWT_SECRET_KEY")
CORS(app)


# parsing the bson into json
def parse_bson(doc):
    return json.loads(json_util.dumps(doc))

# Notes api db
Note = Notes()
User = Users()

# register
# Post /register
@app.route("/register",methods = ["POST"], strict_slashes =False)
def register():
    try:
        credentials = request.get_json()

        # checking for the username and password there in the json body and length not exceeds 2
        if not "username" in credentials.keys() or not "password" in credentials.keys():
            return jsonify({"message":"username and password required"}),401
        
        elif ( len(credentials.keys()) > 2):
            return jsonify({"message":"only username and password valid"}),401

        # if username and password are there in the json body
        else:
            curruname = credentials["username"]
            currpass = credentials["password"].encode("utf-8")

            salt = bcrypt.gensalt()
            currpass = bcrypt.hashpw(password=currpass,salt=salt)

            # if user already exists
            if User.is_user(curruname):
                return jsonify({"message":"user already exists","description":"try another username"}),409
            
            # user creation done
            else:
                User.add_user({"username": curruname, "password": currpass.decode('utf-8')})

                return jsonify({"message":"user created"}),200
        
    except Exception as error:
        return jsonify({"message":f"{error}"}),415
            



# Login 
# POST /login/ required json (username and password)
@app.route('/login', methods=['POST'], strict_slashes = False)
def login():
    
    # check username and password and send back the token
    # running the logic if error occurs throw error through try except block
    try:
        credentials = request.get_json()

        # checking for the username and password there in the json body and length not exceeds 2
        if not "username" in credentials.keys() or not "password" in credentials.keys():
            return jsonify({"message":"username and password required"}),401
        
        # if user passes more fields
        elif ( len(credentials.keys()) > 2):
            return jsonify({"message":"only username and password valid"}),401
        
        # if username and password are there in the json body
        else:
            curruname = credentials["username"]
            currpass = credentials["password"].encode("utf-8")

            user = User.find_user(curruname)
            if user:
                u_dbpass = user["password"].encode("utf-8")
                if bcrypt.checkpw(currpass,u_dbpass):
                    # creating payload for user
                    payload = {"username" : curruname,"id":f"{str(user["_id"])}" ,"exp" : datetime.datetime.utcnow() + timedelta(minutes=20)}

                    # token creating for the user and return
                    token = jwt.encode(payload,getenv("JWT_SECRET_KEY"),getenv("ALGORITHM"))
                    return jsonify({"message":"loggin success", "token":f"{token}"}),200
                
                # if wrong username or password
                else:
                    return jsonify({"message":"bad username or password"}),401
            
            else:
                return jsonify({"message":"bad username or password"}),401


    # if error
    except Exception as error:
        return jsonify({"message":f"{error}"}),415
    
        
# Home page for illustrating how the Note api works
# and its routes
@app.route("/", methods=["GET"])
def home_page():
    return render_template("notes.html")


# Get all notes
# need authorized. GET /notes/ 
@app.route("/notes", methods=['GET'], strict_slashes=False)
@tokenvalidator
def all_notes():

    try:
        data = decodeToken()
        token_user_id = data["id"]
        notes = Note.get_all_notes(token_user_id)
        notes = parse_bson(notes)
        return notes
    except Exception as error:
        return jsonify({"message":"error getting notes", "error":f"{error}"}),500

# Add note 
# need authorized. POST /notes/
@app.route("/notes", methods=['POST'], strict_slashes=False)
@tokenvalidator
def add_notes():
    
    try:
        doc = request.get_json()
        data = decodeToken()

        # taking user id from token for saving with note doc
        tok_user_id = data["id"]

        # check for only one note if any errors
        if "note" not in doc.keys() or len(doc.keys()) > 1:
            return jsonify({f"error":"only one field note required! [note]"}),400
        
        # if the
        else:
            doc = {"userid":f"{tok_user_id}","note": doc["note"]}
            Note.create_note(doc)

            return jsonify({ "message":"note created!" }),201
            414
    except Exception as e:
        return jsonify({"error":f"{e}"}),400

# Update note by its id
# need authorized. PUT /notes/<id> 
# json body of updated document required
@app.route("/notes/<id>", methods=['PUT'])
@tokenvalidator
def update_notes(id):
    
    try:
        note = request.get_json()
        id = ObjectId(id)
        if not note["note"] or len(note.keys()) > 1:
            return jsonify({f"message":"only one field, 'note' required!"}),400
        else:
            updated_note = Note.update_by_id(id, note)
            return jsonify({"message":"note updated", "id":f"{updated_note["_id"]}"}),200
        
    except Exception as e:
        return jsonify({"error":f"{e}"})
    
# Delete note by its id
# need authorized. DELETE /notes/<id> 
@app.route("/notes/<id>", methods = ["DELETE"])
@tokenvalidator
def delete_note(id):

    try:
        id = ObjectId(id)
        note = Note.find_note(id)
        if note:
            collsdb = Note.delete_note(id)
            if collsdb:
                return jsonify({"message":"note deleted!","deletedId":f"{id}"})
        else:
            return jsonify({"message":"note not found", "description":"check the id"}),404

    except Exception as e:
        return jsonify({"error":f"{e}"}),400
    
# Get note by its id
# need authorized. GET /notes/<id> 
@app.route("/notes/<id>", methods = ["GET"])
@tokenvalidator
def get_by_id(id):

    try:
        id = ObjectId(id)

        note = Note.get_note_by_id(id)
        if note:
            note = parse_bson(note)
            return jsonify(note)
        else:
            return jsonify({"message":"note not found", "description":"check the id"}),404
    except Exception as e:
        return jsonify({"error":f"{e}"}),400
    

# error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found',"error_message":f'{error}'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed',"error_message":f'{error}'}), 405

@app.errorhandler(415)
def unsupported_media_type(error):
    return jsonify({'error': 'Unsupported media type', 'error_message':f'{error}'}), 415

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error', 'error_message':f'{error}'}), 500