from abc import ABC

import grpc

from protos.word_game_pb2 import CreateGameRequest, JoinGameRequest, GetPangramRequest, GameStatusRequest, \
    WordSubmissionRequest, InitGameRequest
from protos.word_game_pb2_grpc import WordGameStub

import time


class Menu(ABC):
    def __init__(self, menu_text, menu_options):
        self.menu_text = menu_text
        self.menu_options = menu_options
        self.menu_loop = True

    def display_menu(self):
        print(self.menu_text)

    def run(self):
        while self.menu_loop:
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
        self.menu_loop = False


class GameMenu(Menu):
    def __init__(self, menu_text, menu_options):
        super().__init__(menu_text, menu_options)
        self.channel = grpc.insecure_channel('127.0.0.1:50055')
        self.stub = WordGameStub(self.channel)
        self.game_loop = False
        self.join_game_error_codes = {1: "Invalid join code", 2: "The maximum number of players have been reached",
                                      3: "The username already exists", 4: "The game has already started or finished"}

    def start_game(self, username, game_id):
        print("Starting game...")
        letters = self.stub.GetPangram(GetPangramRequest(gameId=game_id))
        self.game_loop = True
        while self.game_loop:
            print(letters)
            word = input("Enter a word (or enter \\s to see the game status): ")
            if word == "\\s":
                status = self.stub.QueryGameStatus(GameStatusRequest(gameId=game_id))
                self.print_status(status)
            else:
                response = self.stub.SubmitWord(WordSubmissionRequest(gameId=game_id, username=username,
                                                                      word=word.lower()))
                print(response.message, "- Score:", response.score, "Total:", response.total)

    def print_status(self, status):
        print("GAME STATE:")
        for i in range(len(status.usernames)):
            user = status.usernames[i]
            words = status.words[user].word
            print(f"User: {user}, Score: {status.scores[i]}, Words found: {words}")

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


class GameMainMenu(GameMenu):
    def __init__(self):
        self.menu_text = "SpellingBeeGame!!\n" \
                         "1. Create a new game\n" \
                            "2. Join an existing game\n" \
                            "3. Quit"
        self.menu_options = {"1": self.create_new_game, "2": self.join_existing_game, "3": self.exit_menu}
        super().__init__(self.menu_text, self.menu_options)

    def create_new_game(self):
        submenu = CreateGameMenu()
        submenu.run()

    def join_existing_game(self):
        username = self._create_username()
        join_code = input("Enter the join code: ")

        join_game_response = self.stub.JoinGame(JoinGameRequest(username=username, joinCode=join_code))
        join_response_code = join_game_response.responseCode

        # only joins the game if the response code is 0. Otherwise an error will be thrown
        if join_response_code == 0:
            game_id = join_game_response.gameId
            print("Joining game...")
            print("Waiting for the main player to initiate game...")
            time.sleep(5)
            self.start_game(username, game_id)
        else:
            print("Cannot join the game - Error: ", end="")
            print(self.join_game_error_codes[join_response_code])


class CreateGameMenu(GameMenu):
    def __init__(self):
        self.game_type = "SpellingBee"
        self.menu_text = "Create a new game:\n" \
                         "1. Singleplayer game\n" \
                         "2. Multiplayer game (2 player co-operative)\n" \
                         "3. Back to main menu"
        self.menu_options = {"1": self.create_singleplayer_game, "2": self.create_multiplayer_coop_game,
                             "3": self.exit_menu}
        super().__init__(self.menu_text, self.menu_options)

    def create_singleplayer_game(self):
        game_mode = "Single"
        print("Creating singleplayer game")
        username = self._create_username()
        game_id = self.stub.CreateGame(CreateGameRequest(username=username, gameType=self.game_type,
                                                         gameMode=game_mode)).gameId
        self.stub.InitGame(InitGameRequest(gameId=game_id))
        self.start_game(username, game_id)

    def create_multiplayer_coop_game(self):
        game_mode = "MultiCoop"
        print("Creating multiplayer cooperative game")
        username = self._create_username()
        create_game_response = self.stub.CreateGame(CreateGameRequest(username=username,
                                                                      gameType=self.game_type,
                                                                      gameMode=game_mode))
        game_id = create_game_response.gameId
        join_code = create_game_response.joinCode
        response_code = self.stub.InitGame(InitGameRequest(gameId=game_id)).responseCode

        # waits for the second player to join
        while response_code == 1:
            print(f"Waiting for another player to join - join code: {join_code}")
            time.sleep(5)
            response_code = self.stub.InitGame(InitGameRequest(gameId=game_id)).responseCode
        self.start_game(username, game_id)


menu = GameMainMenu()
menu.run()
