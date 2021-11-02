import logging
from concurrent import futures

import grpc

from domain.word_game import SpellingBeeGameBuilder
from word_game_pb2 import GameResponse, InitResponse, WordSubmissionResponse
from word_game_pb2_grpc import WordGameServicer, add_WordGameServicer_to_server
from services.game_registry import GameRegistry
from factories.object_factory import ObjectFactory
from services.lookup_service import JSONLookupServiceBuilder

class WordGameServer(WordGameServicer):

    dictionaries = {"word_dict": "words_dictionary.json",
                    "pangram_dict": "pangrams.json"}

    def __init__(self):
        self.game_type = "SpellingBee"
        self.lookup_service_type = "JSON"
        self.factory = ObjectFactory()
        self.factory.register_builder(self.lookup_service_type, JSONLookupServiceBuilder())
        self.factory.register_builder(self.game_type, SpellingBeeGameBuilder())
        self.registry = GameRegistry.get_instance()

    def CreateGame(self, request, context):
        lookup_service = self.factory.create(self.lookup_service_type, source_files_dict=self.dictionaries)
        game = self.factory.create(request.gameType, word_lookup_service=lookup_service)
        game_id = self.registry.add_game(game)
        print("Created game with id " + str(game_id.bytes))
        return GameResponse(gameId=game_id.bytes)

    def InitGameRequest(self, request, context):
        game = self.registry.get_game(request.gameId)
        game.setup_game()
        pangram = game.start_game()
        return InitResponse(letters=pangram)

    def SubmitWord(self, request, context):
        game = self.registry.get_game(request.gameId)
        score, total, message = game.check_word(request.word)
        return WordSubmissionResponse(score=score, total=total, message=message)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_WordGameServicer_to_server(WordGameServer(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()

