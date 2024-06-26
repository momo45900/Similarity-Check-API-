from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import spacy

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB
Users = db["Users"]
Admin = db["Admin"]

def UserExists(username):
    return Users.count_documents({"username": username}) > 0

def AdminExists(username):
    return Admin.count_documents({"username": username}) > 0

def verify(username, password):
    if not UserExists(username):
        return False

    hashed_pw = Users.find_one({"username": username})["password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def verify_admin(username, password):
    if not AdminExists(username):
        return False

    hashed_pw = Admin.find_one({"username": username})["password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def countTokens(username):
    tokens = Users.find_one({"username": username})["tokens"]
    return tokens

class Register(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]

        if UserExists(username):
            ret = {
                "status": "301",
                "msg": "Invalid username"
            }
            return jsonify(ret)

        hashed_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

        Users.insert_one({
            "username": username,
            "password": hashed_pw,
            "tokens": 6
        })

        ret = {
            "status": "200",
            "msg": "You have been registered successfully"
        }
        return jsonify(ret)

class Detect(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        text1 = postedData["text1"]
        text2 = postedData["text2"]

        correct_user_and_pw = verify(username, password)

        if not correct_user_and_pw:
            ret = {
                "status": "302",
                "msg": "Invalid username or password"
            }
            return jsonify(ret)

        num_tokens = countTokens(username)

        if num_tokens <= 0:
            ret = {
                "status": "303",
                "msg": "Out of tokens"
            }
            return jsonify(ret)

        nlp = spacy.load('en_core_web_sm')
        doc1 = nlp(text1)
        doc2 = nlp(text2)
        ratio = doc1.similarity(doc2)

        Users.update_one({"username": username}, {"$set": {"tokens": num_tokens - 1}})

        retJson = {
            "status": 200,
            "similarity": ratio,
            "msg": "Similarity score calculated successfully"
        }
        return jsonify(retJson)

class AdminRegister(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]

        if AdminExists(username):
            ret = {
                "status": "301",
                "msg": "Invalid username"
            }
            return jsonify(ret)

        hashed_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

        Admin.insert_one({
            "username": username,
            "password": hashed_pw,
        })

        ret = {
            "status": "200",
            "msg": "You have been registered successfully"
        }
        return jsonify(ret)

class Refill(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        refilled_user = postedData["refilled_user"]
        amount = postedData["amount"]

        correct_user_and_pw = verify_admin(username, password)

        if not correct_user_and_pw:
            ret = {
                "status": "302",
                "msg": "Invalid username or password"
            }
            return jsonify(ret)

        current_tokens = countTokens(refilled_user)
        Users.update_one({"username": refilled_user}, {"$set": {"tokens": amount + current_tokens}})

        ret = {
            "status": "200",
            "msg": "Successfully refilled the tokens"
        }
        return jsonify(ret)

api.add_resource(Register, '/register')
api.add_resource(Detect, '/detect')
api.add_resource(Refill, '/refill')
api.add_resource(AdminRegister, '/admin')

if __name__ == "__main__":
    app.run(debug=True)