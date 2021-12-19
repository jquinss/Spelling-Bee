from abc import ABC, abstractmethod
import pika
import json


class Observer(ABC):
    @abstractmethod
    def update(self, observable, arg):
        pass


# class used to send the stats to the RabbitMQ queue
class MessageQueueSender:
    def __init__(self, queue_name, hostname="127.0.0.1"):
        self.hostname = hostname
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.hostname))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue_name)

    def reconnect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.hostname))
        self.channel = self.connection.channel()
        self.channel.queue_declare(self.queue_name)

    def send(self, message):
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=message)

    def close_connection(self):
        self.connection.close()


# implements the Observer abstract class. Will be updated by the WordGameServer whenever the user scores
class GameStatsQueueProcessor(Observer):
    def __init__(self, queue_sender):
        self.queue_sender = queue_sender

    def update(self, server, game_id):
        # calls the get_game_status method to get the stats from the observable (WordGameServer)
        game_status = server.get_game_status(game_id)
        self.queue_sender.send(json.dumps(game_status))
