from abc import ABC

class Menu(ABC):
    def __init__(self):
        self.menu_loop = True

    def show_menu(self):
        pass

    def loop(self):
        while self.menu_loop:
            self.show_menu()
            self.request_input("Select an option: ")

    def request_input(self, prompt):
        pass

    def process_selection(self, selection):
        pass

    def exit_menu(self):
        self.menu_loop = False
        print("Exiting menu")
        exit()



class SpellingBeeClientMenu(Menu):
    MENU = """The SpellingBee
    1) Start game
    2) Quit game"""

    def __init__(self):
        super().__init__()
        self.choices = {"1": self.start_game, "2": self.exit_menu}

    def show_menu(self):
        print(self.MENU)

    def request_input(self, prompt):
        choice = input(prompt)
        self.process_selection(choice)

    def process_selection(self, choice):
        print("You selected ", str(choice))
        action = self.choices.get(choice)
        if action:
            action()
        else:
            "That is not a valid choice"

    def start_game(self):
        game_loop = True
        print("You selected to start the game")

menu = SpellingBeeClientMenu()
menu.loop()