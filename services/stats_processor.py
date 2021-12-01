from abc import ABC, abstractmethod
import pika


class Observer(ABC):
    @abstractmethod
    def update(self, observable, arg):
        pass


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


class GameStatsQueueProcessor(Observer):
    def __init__(self, stats_queue):
        self.stats_queue = stats_queue

    def update(self, server, game_id):
        game_status = server.get_game_status(game_id)
        self.stats_queue.send(game_status)
