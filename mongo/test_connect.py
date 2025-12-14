from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv(".env")

client = MongoClient(os.environ.get("MONGO_URI"))

try:
    result = client.admin.command("ping")
    print("Successfully connected!")
    print(result)
except Exception as e:
    print(e)