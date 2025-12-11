from pymongo import MongoClient
from .config import settings

client = MongoClient(settings.MONGODB_URI)
db = client[settings.MONGODB_DB_NAME]

# Collections in master DB
organizations_collection = db["organizations"]
admins_collection = db["admins"]

