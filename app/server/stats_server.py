import pika
from threading import Thread
import socket
import json


class MessageQueueConsumer(Thread):
    def __init__(self, queue_name, hostname="localhost", callback=None):
        Thread.__init__(self)
        self.hostname = hostname
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.hostname))
        self.channel = self.connection.channel()
        self.channel.queue_declare(self.queue_name)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    def run(self):
        self.channel.start_consuming()


class StatsServer:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.stats_list = []
        self.clients = []
        self.msg_consumer = MessageQueueConsumer("SpellingBee", callback=self.consume_stats)

    def consume_stats(self, ch, method, properties, body):
        stats = json.loads(body)
        self.stats_list.append(stats)
        self.send_stats(stats)

    def send_all_stats(self, client):
        for stats in self.stats_list:
            client.sendall(json.dumps(stats))

    def send_stats(self, stats):
        for client in self.clients:
            client.sendall(json.dumps(stats))

    def run(self):
        self.msg_consumer.start()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.hostname, self.port))
            while True:
                sock.listen()
                client_conn, address = sock.accept()
                self.clients.append(client_conn)
                self.send_all_stats(client_conn)


StatsServer("localhost", 65512).run()
