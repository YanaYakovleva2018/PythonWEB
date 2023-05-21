import pika
from faker import Faker
from random import choice

from models import Client

fake = Faker("uk_UA")

def seed_clients():
    for _ in range(30):
        contact = Client(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            address=fake.address(),
            prefer_method=choice(["SMS", "Email"])
        )
        contact.save()
        
def main():
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue="email_queue")
    channel.queue_declare(queue="sms_queue")

    contacts = Client.objects()

    for contact in contacts:
        message = str(contact.id)
        if contact.prefer_method == "SMS":
            channel.basic_publish(exchange="", routing_key="sms_queue", body=message)
        elif contact.prefer_method == "Email":
            channel.basic_publish(exchange="", routing_key="email_queue", body=message)
    connection.close()

if __name__ == '__main__':
    seed_clients()
    main()
