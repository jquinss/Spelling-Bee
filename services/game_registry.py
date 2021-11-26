import uuid
import threading
import string
import random


class GameRegistry:
    __instance = None

    def __init__(self):
        if GameRegistry.__instance is not None:
            raise Exception("This is a singleton!")
        else:
            GameRegistry.__instance = self
        self.lock = threading.Lock()
        self.games = {}
        self.instance = None

    @staticmethod
    def get_instance():
        if GameRegistry.__instance is None:
            with threading.Lock():
                if GameRegistry.__instance is None:
                    GameRegistry()
        return GameRegistry.__instance

    def add_game(self, game):
        self.lock.acquire()
        game_id = self._generate_game_id()
        while game_id in self.games:
            game_id = self._generate_game_id()
        self.games[game_id] = game
        self.lock.release()
        return game_id

    def get_game(self, game_id):
        return self.games[uuid.UUID(bytes=game_id)]

    def _generate_game_id(self, size=9, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
