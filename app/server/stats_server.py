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
        self.stats_list = []
        self.clients = []
        self.msg_consumer = MessageQueueConsumer("test", callback=self.consume_stats)
        self.server_socket = self.init_socket(hostname, port)

    def init_socket(self, hostname, port):
        sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sck.bind((hostname, port))
        return sck

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
        while True:
            self.server_socket.listen()
            client_conn, address = self.server_socket.accept()
            self.clients.append(client_conn)
            self.send_all_stats(client_conn)


StatsServer("localhost", 65512).run()
