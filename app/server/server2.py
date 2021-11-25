import logging
import string
import random
from concurrent import futures

import grpc

from domain.word_game import WordGameFactoryBuilder, SpellingBeeGameFactory, MultiCoopSpellingBeeGame, \
    MinPlayersRequiredError, MaxPlayersLimitReachedError, UsernameAlreadyExistsError, GameStateError
from word_game2_pb2 import CreateGameResponse, InitGameResponse, WordSubmissionResponse, JoinGameResponse, \
    GetPangramResponse, GameStatusResponse
from word_game2_pb2_grpc import WordGameServicer, add_WordGameServicer_to_server
from services.game_registry import GameRegistry
from services.lookup_service import LookupServiceFactory


class WordGameServer(WordGameServicer):

    dictionaries = {"word_dict": "../../data/words_dictionary.json",
                    "pangram_dict": "../../data/pangrams.json"}

    def __init__(self):
        self.lookup_service_factory = LookupServiceFactory()
        self.lookup_service = self.lookup_service_factory.create_lookup_service("JSON",
                                                                                source_files_dict=self.dictionaries)
        self.game_factory_builder = WordGameFactoryBuilder()
        self.game_factory_builder.register_word_game_factory(SpellingBeeGameFactory(self.lookup_service), "SpellingBee")
        self.registry = GameRegistry.get_instance()
        self.join_codes = {}

    def CreateGame(self, request, context):
        factory = self.game_factory_builder.get_word_game_factory(request.gameType)
        game = factory.create_game(request.gameMode)
        game.add_player(request.username)
        game_id = self.registry.add_game(game)
        join_code = ""
        if isinstance(game, MultiCoopSpellingBeeGame):
            while join_code not in self.join_codes:
                join_code = self._generate_join_code()
            self.join_codes[join_code] = game_id
        return CreateGameResponse(gameId=game_id.bytes, joinCode=join_code)

    def InitGame(self, request, context):
        game = self.registry.get_game(request.gameId)
        response_code = 0
        try:
            game.setup_game()
            game.start_game()
        except MinPlayersRequiredError:
            response_code = 1
        return InitGameResponse(responseCode=response_code)

    def JoinGame(self, request, context):
        join_code = request.join_code
        username = request.username
        response_code = 0
        if join_code not in self.join_codes:
            response_code = 1
        game_id = self.join_codes[join_code]
        game = self.registry.get_game(game_id)
        try:
            game.add_player(username)
        except MaxPlayersLimitReachedError:
            response_code = 2
        except UsernameAlreadyExistsError:
            response_code = 3
        except GameStateError:
            response_code = 4
        return JoinGameResponse(responseCode=response_code, gameId=game_id)

    def GetPangram(self, request, context):
        game = self.registry.get_game(request.gameId)
        return GetPangramResponse(letters=game.get_pangram_letters())

    def SubmitWord(self, request, context):
        game = self.registry.get_game(request.gameId)
        score, total, message = game.check_word(request.word, request.player)
        return WordSubmissionResponse(score=score, total=total, message=message)

    def QueryGameStatus(self, request, context):
        game = self.registry.get_game(request.gameId)
        return GameStatusResponse(statusInfo=game.get_game_status())

    def _generate_join_code(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_WordGameServicer_to_server(WordGameServer(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()

