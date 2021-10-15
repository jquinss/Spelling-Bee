import uuid
import threading


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
        game_id = uuid.uuid4()
        self.games[game_id] = game
        self.lock.release()
        return game_id

    def get_game(self, game_id):
        return self.games[uuid.UUID(bytes=game_id)]
