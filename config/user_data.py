import os, dotenv
from pymongo import MongoClient
import pymongo
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
mongodb_connection = os.getenv('MONGODB_CONNECT')

client = MongoClient(mongodb_connection)
db_connection = client["izzie"]
collection = db_connection.get_collection("users")
server_collection = db_connection.get_collection("servers")

class userdata:
    def __init__(self, db_connection) -> None:
        self.__collection_name = "users"
        self.__db_connection = db_connection
    def openaccount(id):
        if collection.find_one({ "discord_id": id }):
            return True
        else:
            docs = { "discord_id": id, "saldo": 0, "reps": 0, "bg": None, "sobremim": "Use /sobremim para trocar essa mensagem" }
            collection.insert_one(docs)
            return docs