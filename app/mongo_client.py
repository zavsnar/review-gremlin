from pymongo import MongoClient


# MongoDB Configuration
MONGODB_URI = "mongodb://127.0.0.1:27017/mydb"  # Use the service name 'mongo'
client = MongoClient(MONGODB_URI)
db = client.mydb
review_collection = db.mycollection