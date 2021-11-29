import pika
import json


class MessageQueueSender:
    def __init__(self, queue_name, hostname="localhost"):
        self.hostname = hostname
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.hostname))
        self.channel = self.connection.channel().queue_declare(queue_name)

    def reconnect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.hostname))
        self.channel = self.connection.channel().queue_declare(self.queue_name)

    def send(self, routing_key, message):
        self.channel.basic_publish(exchange='', routing_key=routing_key, body=message)

    def close_connection(self):
        self.connection.close()