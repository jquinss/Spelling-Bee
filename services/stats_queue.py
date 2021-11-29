import pika
import json


class StatsQueue:
    def __init__(self, hostname="localhost", queue_name="spellingbee"):
        self.hostname = hostname
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.hostname))
        self.channel = self.connection.channel().queue_declare(queue_name)

    def reconnect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.hostname))
        self.channel = self.connection.channel().queue_declare(self.queue_name)

    def send(self, routing_key, stats_dict):
        self.channel.basic_publish(exchange='', routing_key=routing_key, body=json.dumps(stats_dict))

    def close_connection(self):
        self.connection.close()