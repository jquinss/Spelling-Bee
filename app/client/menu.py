from abc import ABC, abstractmethod


class Menu(ABC):
    def __init__(self, menu_text):
        self.menu_text = menu_text
        self.keep_looping = True

    def display_menu(self):
        print(self.menu_text)

    def run(self):
        while self.keep_looping:
            self.display_menu()
            choice = input("Enter an option: ")
            self.process_selection(choice)

    @abstractmethod
    def process_selection(self, choice):
        pass


class ClientMenu(Menu):
    def __init__(self):
        self.menu_text = "1. Create a new game\n" \
                            "2. Join an existing game\n" \
                            "3. Quit"
        super().__init__(self.menu_text)
        self.options = {"1": self.start_game, "2": self.join_game, "3": self.exit_menu}

    def start_game(self):
        print("Starting game")

    def join_game(self):
        print("Joining game")

    def process_selection(self, choice):
        action = self.options.get(choice)
        if action:
            action()
        else:
            print("{0} is not a valid choice".format(choice))

    def exit_menu(self):
        print("Exiting menu")
        self.keep_looping = False
