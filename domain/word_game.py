from abc import ABC, abstractmethod
from random import shuffle
from utils.formatter import Formatter
from threading import Lock
from enum import Enum


class GameManager(ABC):
    @abstractmethod
    def setup_game(self):
        """Primitive operation. It needs to be overriden."""
        pass

    @abstractmethod
    def start_game(self):
        """Primitive operation. It needs to be overriden."""
        pass

    @abstractmethod
    def end_game(self):
        """Primitive operation. It needs to be overriden."""
        pass


class WordGameTemplate(ABC):
    def __init__(self, word_lookup_service):
        self.word_lookup_service = word_lookup_service
        self.players = {}
        self.words_found_list = {}

    @abstractmethod
    def calculate_word_score(self, word):
        """Primitive operation. It needs to be overriden. Different games may use different criteria to calculate the
        score"""
        pass

    @abstractmethod
    def evaluate_word(self, word):
        """Primitive operation. It needs to be overriden. Different games may use different criteria to evaluate the
        word (e.g. check if the word is valid or not)"""
        pass

    def is_word_in_dictionary(self, word, dictionary_key):
        if self.word_lookup_service.lookup_entry(dictionary_key, word) is not None:
            return True
        return False

    def check_word(self, word, player):
        """
            :param word: word chosen by the player
            :param player: player username
            :return:
                    - score - word score
                    - total_score - total score so far
                    - message - informational message (e.g. valid word, pangram, etc.)
        """
        score = 0
        is_valid_word, message = self.evaluate_word(word)
        if is_valid_word:
            score = self.calculate_word_score(word)
            self.words_found_list[word] = score
            self.players[player]["words"].append(word)
            self.players[player]["total"] += score
        return score, self.players[player]["total"], message


class SpellingBeeGame(WordGameTemplate, GameManager):
    MIN_WORD_LEN = 4
    PANGRAM_LEN = 7
    PANGRAM_BONUS = 7
    REQUIRED_LETTER_INDEX = 3

    def __init__(self, word_lookup_service=None, max_players=1, min_players=1):
        super().__init__(word_lookup_service)
        self.pangram_letters = []
        self.max_players = max_players
        self.min_players = min_players
        self.state = GameState.SET_UP
        self.lock2 = Lock()

    def add_player(self, player):
        # we do not want to allow more than one thread to access this method simultaneously
        with self.lock2:
            if len(self.players) >= self.max_players:
                raise MaxPlayersLimitReachedError()
            if player in self.players:
                raise UsernameAlreadyExistsError()
            if self.state != GameState.SET_UP:
                raise GameStateError(self.state)
            self.players[player] = {}

    def setup_game(self):
        if len(self.players) < self.min_players:
            raise MinPlayersRequiredError()
        if self.state != GameState.SET_UP:
            raise GameStateError(self.state)
        for player in self.players:
            self.players[player]["total"] = 0
            self.players[player]["words"] = []
        self.state = GameState.START

    def start_game(self):
        if self.state != GameState.START:
            raise GameStateError(self.state)
        pangram = self.word_lookup_service.get_random_entry_index("pangram_dict")
        self.pangram_letters = self.randomize_word(pangram)

    def end_game(self):
        self.state = GameState.FINISH

    def get_pangram_letters(self):
        return self.format_pangram_output(self.pangram_letters)

    def get_game_status(self):
        status = {"pangram": self.pangram_letters, "players": self.players,
                  "words_found": self.words_found_list}

        return status

    def randomize_word(self, word):
        letters = list(set(word))
        shuffle(letters)
        return letters

    def check_word(self, word, player):
        # we do not want to allow more than one thread to access this method simultaneously
        with self.lock2:
            if self.state != GameState.START:
                raise GameStateError(self.state)
            return super().check_word(word, player)

    def calculate_word_score(self, word):
        """
            :param word: word chosen by the player
            :return: score: word score
        """
        word_len = len(word)
        if word_len == self.MIN_WORD_LEN:
            return 1
        else:
            pangram_letters_set = set(self.pangram_letters)
            word_letters_set = set(word)
            if word_len >= self.MIN_WORD_LEN and not pangram_letters_set.issubset(word_letters_set):
                return word_len
            elif pangram_letters_set.issubset(word_letters_set):
                return self.PANGRAM_LEN + self.PANGRAM_BONUS + (word_len - self.PANGRAM_LEN)
        return 0

    def evaluate_word(self, word):
        """
            :param word: word chosen by the player
            :return:
                    - boolean - word is valid or not
                    - message - informational message (e.g. valid word, pangram, etc.)
        """
        if word in self.words_found_list:
            return False, "The word {} has already been found".format(word)

        word_letters_set = set(word)
        pangram_letters_set = set(self.pangram_letters)

        if len(word) < self.MIN_WORD_LEN or not word_letters_set.issubset(pangram_letters_set) or \
                not self.is_word_in_dictionary(word, "word_dict"):
            return False, "Sorry, that is not a valid word"

        center_letter = self.pangram_letters[self.REQUIRED_LETTER_INDEX]

        if self.pangram_letters[self.REQUIRED_LETTER_INDEX] not in word:
            return False, "Invalid word, missing centre letter {}".format(center_letter)

        if word_letters_set.issubset(pangram_letters_set):
            if pangram_letters_set.issubset(word_letters_set):
                return True, "Pangram!"
            else:
                return True, "Valid word"

        return False, "Sorry that is not a valid word"

    # formats raw pangram for sending to the player
    def format_pangram_output(self, iterable):
        formatted_pangram = Formatter.iterable_to_string(iterable, separator=" ")
        middle_letter = int((len(formatted_pangram) - 1) / 2)
        formatted_pangram = Formatter.insert_into_string({middle_letter: "[", middle_letter + 1: "]"},
                                                         formatted_pangram).upper()
        return formatted_pangram


class MultiCoopSpellingBeeGame(SpellingBeeGame):
    def __init__(self, word_lookup_service=None, max_players=2):
        super().__init__(word_lookup_service=word_lookup_service, min_players=2, max_players=max_players)
        self.lock1 = Lock()

    def check_word(self, word, player):
        # we do not want to allow more than one thread to access this method simultaneously
        with self.lock1:
            score, player_total, message = super().check_word(word, player)
            # in the coop game we set the total score for each player to be the same
            if score > 0:
                for pl in self.players:
                    self.players[pl]["total"] = player_total
            return score, player_total, message


# created factories
class WordGameFactoryBuilder:
    def __init__(self):
        self.factories = {}

    def register_word_game_factory(self, factory, name):
        self.factories[name] = factory

    def get_word_game_factory(self, name):
        factory = self.factories.get(name)
        if not factory:
            raise ValueError(name)
        return factory


class WordGameFactory(ABC):
    def __init__(self, word_lookup_service):
        self.word_lookup_service = word_lookup_service

    @abstractmethod
    def create_game(self, game_mode, **kwargs):
        pass


class SpellingBeeGameFactory(WordGameFactory):
    def __init__(self, word_lookup_service):
        super().__init__(word_lookup_service)

    def create_game(self, game_mode, **kwargs):
        if game_mode == 'Single':
            return SpellingBeeGame(word_lookup_service=self.word_lookup_service)
        elif game_mode == 'MultiCoop':
            return MultiCoopSpellingBeeGame(word_lookup_service=self.word_lookup_service, **kwargs)
        else:
            raise ValueError(game_mode)


# Defined exceptions for different situations of the game (e.g. trying to add more players that the max number allowed,
# trying to create a username that already exists, etc.)
class MaxPlayersLimitReachedError(Exception):
    pass


class MinPlayersRequiredError(Exception):
    pass


class UsernameAlreadyExistsError(Exception):
    pass


# defined enum with the different game states
class GameState(Enum):
    SET_UP = 1
    START = 2
    FINISH = 3


class GameStateError(Exception):
    def __init__(self, game_state):
        super().__init__(f"Invalid action for the current game state (STATE: {game_state})")