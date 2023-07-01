from pymongo import MongoClient

def get_mongodb():
    client = MongoClient("mongodb+srv://yanayakovleva362:186326abc@cluster0.ybqwg3o.mongodb.net/")

    db = client.hw
    return db