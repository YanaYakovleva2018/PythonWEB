import pika
from mongoengine import connect, DoesNotExist

from models import Client

connect(host="mongodb+srv://yanayakovleva362:186326abc@cluster0.ybqwg3o.mongodb.net/?retryWrites=true&w=majority")

def main():
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue="sms_queue")

    def callback(ch, method, properties, body):
        try:
            message = body.decode()
            contact = Client.objects.get(id=message)
            print(f"A new SMS-message has been received {message}")
            contact.send_message = True
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except DoesNotExist:
            print(f"Could not send a SMS-message")

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="sms_queue", on_message_callback=callback)
    print("Waiting for SMS-messages")
    channel.start_consuming()

if __name__ == "__main__":
    main()