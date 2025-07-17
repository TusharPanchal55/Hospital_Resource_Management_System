from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")  # or your MongoDB URI
db = client['hospital_db']  # your database name

# collections
users_collection = db['users']
usage_collection = db['resources']
