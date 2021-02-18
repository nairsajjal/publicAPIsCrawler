import json
import pymongo

url = "mongodb+srv://admin:PLmn%40321@cluster0.ydmi9.mongodb.net/apiCrawler?retryWrites=true&w=majority"
connection = pymongo.MongoClient(url)
db = connection["apiCrawler"]
collection = db["data"]

with open('data.json', 'r') as f:
    file_data = json.load(f)
try:
    collection.insert_one(file_data)
except pymongo.errors.ServerSelectionTimeoutError as e:
    print("Couldn't connect to the Database .. ", e)
connection.close()