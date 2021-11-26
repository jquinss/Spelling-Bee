from abc import ABC

import grpc

import word_game2_pb2
import word_game2_pb2_grpc

import time

class Menu(ABC):
    def __init__(self, menu_text, menu_options):
        self.menu_text = menu_text
        self.menu_options = menu_options
        self.keep_looping = True

    def display_menu(self):
        print(self.menu_text)

    def run(self):
        while self.keep_looping:
            self.display_menu()
            choice = input("Enter an option: ")
            self.process_selection(choice)

    def process_selection(self, choice):
        action = self.menu_options.get(choice)
        if action:
            action()
        else:
            print("{0} is not a valid choice".format(choice))

    def exit_menu(self):
        self.keep_looping = False


class GameMainMenu(Menu):
    def __init__(self):
        self.menu_text = "1. Create a new game\n" \
                            "2. Join an existing game\n" \
                            "3. Quit"
        self.menu_options = {"1": self.create_new_game, "2": self.join_existing_game, "3": self.exit_menu}
        super().__init__(self.menu_text, self.menu_options)
        self.channel = grpc.insecure_channel('127.0.0.1:50055')
        self.stub = word_game2_pb2_grpc.WordGameStub(self.channel)


    def create_new_game(self):
        print("Entering create new game sub-menu")
        submenu = CreateGameMenu(self.stub)
        submenu.run()

    def join_existing_game(self):
        username = self._create_username()
        join_code = input("Enter the join code: ")

        join_game_response = self.stub.JoinGame(word_game2_pb2.JoinGameRequest(username=username, joinCode=join_code))

        join_response_code = join_game_response.responseCode

        if join_response_code == 0:
            game_id = join_game_response.gameId
            print("joining game. Waiting for the main player to initiate game")
            time.sleep(5)
            letters = self.stub.GetPangram(word_game2_pb2.GetPangramRequest(gameId=game_id))
            self.game_loop = True
            while self.game_loop:
                print(letters)
                word = input("Enter a word (or command - enter \\h for a list of available commands): ")
                if word == "\\s":
                    status = self.stub.QueryGameStatus(word_game2_pb2.GameStatusRequest(gameId=game_id))
                    print(status)
                else:
                    print("submitted word " + word)
                    response = self.stub.SubmitWord(word_game2_pb2.WordSubmissionRequest(gameId=game_id,
                                                                                              username=username,
                                                                                              word=word.lower()))
                    print(response.message, "- Score:", response.score, "Total:", response.total)


    def _create_username(self):
        valid_user = False
        username = ""
        while not valid_user:
            username = input("Create a username: ")
            if username == "":
                print("Username cannot be empty")
            else:
                valid_user = True
        return username


class CreateGameMenu(Menu):
    def __init__(self, game_stub):
        self.game_type = "SpellingBee"
        self.game_loop = False
        self.game_stub = game_stub
        self.menu_text = "1. Singleplayer game\n" \
                         "2. Multiplayer game (2 player co-operative)\n" \
                         "3. Back to main menu"
        self.menu_options = {"1": self.create_singleplayer_game, "2": self.create_multiplayer_coop_game,
                             "3": self.exit_menu}
        super().__init__(self.menu_text, self.menu_options)

    def create_singleplayer_game(self):
        game_mode = "Single"
        print("Creating singleplayer game")
        print("Requesting username")
        username = self._create_username()
        game_id = self.game_stub.CreateGame(word_game2_pb2.CreateGameRequest(username=username,
                                            gameType=self.game_type, gameMode=game_mode)).gameId
        self.game_stub.InitGame(word_game2_pb2.InitGameRequest(gameId=game_id))
        letters = self.game_stub.GetPangram(word_game2_pb2.GetPangramRequest(gameId=game_id))
        self.game_loop = True
        while self.game_loop:
            print(letters)
            word = input("Enter a word (or command - enter \\h for a list of available commands): ")
            if word == "\\s":
                status = self.game_stub.QueryGameStatus(word_game2_pb2.GameStatusRequest(gameId=game_id))
                print(status)
            else:
                response = self.game_stub.SubmitWord(word_game2_pb2.WordSubmissionRequest(gameId=game_id,
                                                                username=username, word=word.lower()))
                print(response.message, "- Score:", response.score, "Total:", response.total)

    def create_multiplayer_coop_game(self):
        game_mode = "MultiCoop"
        print("Creating multiplayer cooperative game")
        print("Requesting username")
        username = self._create_username()
        create_game_response = self.game_stub.CreateGame(word_game2_pb2.CreateGameRequest(username=username,
                                                                             gameType=self.game_type,
                                                                             gameMode=game_mode))
        game_id = create_game_response.gameId
        join_code = create_game_response.joinCode
        response_code = self.game_stub.InitGame(word_game2_pb2.InitGameRequest(gameId=game_id)).responseCode
        while response_code == 1:
            print(f"Waiting for another player to join - join code: {join_code}")
            time.sleep(5)
            response_code = self.game_stub.InitGame(word_game2_pb2.InitGameRequest(gameId=game_id)).responseCode
        print("Starting game")

        letters = self.game_stub.GetPangram(word_game2_pb2.GetPangramRequest(gameId=game_id))
        self.game_loop = True
        while self.game_loop:
            print(letters)
            word = input("Enter a word (or command - enter \\h for a list of available commands): ")
            if word == "\\s":
                status = self.game_stub.QueryGameStatus(word_game2_pb2.GameStatusRequest(gameId=game_id))
                print(status)
            else:
                print("Submitted word " + word)
                response = self.game_stub.SubmitWord(word_game2_pb2.WordSubmissionRequest(gameId=game_id,
                                                                                          username=username,
                                                                                          word=word.lower()))
                print(response.message, "- Score:", response.score, "Total:", response.total)

    def _create_username(self):
        valid_user = False
        username = ""
        while not valid_user:
            username = input("Create a username: ")
            if username == "":
                print("Username cannot be empty")
            else:
                valid_user = True
        return username


menu = GameMainMenu()
menu.run()