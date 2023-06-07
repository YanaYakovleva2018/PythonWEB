import json
from bson.objectid import ObjectId

from pymongo import MongoClient

client = MongoClient("mongodb+srv://yanayakovleva362:186326abc@cluster0.ybqwg3o.mongodb.net/")

db = client.hw

with open('quotes.json', encoding='utf-8') as fd:
    quotes = json.load(fd)


for quote in quotes:
    author = db.authors.find_one({'fullname': quote['author']})
    if author:
        db.quotes.insert_one({
            'quote':  quote['quote'],
            'tags':  quote['tags'],
            'author': ObjectId(author['_id'])
        })
