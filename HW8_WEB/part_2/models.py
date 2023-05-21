from mongoengine import connect, Document, StringField, BooleanField

connect(host="mongodb+srv://yanayakovleva362:186326abc@cluster0.ybqwg3o.mongodb.net/?retryWrites=true&w=majority")

class Client(Document):
    name = StringField()
    email = StringField()
    phone = StringField()
    address = StringField()
    send_message = BooleanField()
    prefer_method = StringField()