from mongoengine import connect, Document, CASCADE
from mongoengine.fields import  ListField, StringField, ReferenceField

connect(
    host="mongodb+srv://yanayakovleva362:186326abc@cluster0.ybqwg3o.mongodb.net/?retryWrites=true&w=majority")


class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    quote = StringField()
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField()
    meta = {'allow_inheritance': True}