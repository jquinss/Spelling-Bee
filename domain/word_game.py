from abc import ABC, abstractmethod
from random import shuffle
from services.lookup_service import JSONLookupService

class WordGameTemplate(ABC):
    def __init__(self, word_lookup_service):
        self.word_lookup_service = word_lookup_service
        self.players = []
        self.words_found_list = []
        self.scores = []
        self.total_scores = []
        self.current_player_index = -1

    @abstractmethod
    def register_player(self, username):
        pass

    @abstractmethod
    def setup_game(self):
        pass

    @abstractmethod
    def start_game(self):
        pass

    @abstractmethod
    def end_game(self):
        pass

    @abstractmethod
    def calculate_score(self, word):
        pass

    @abstractmethod
    def evaluate_word(self, word):
        pass

    def is_in_dictionary(self, word, dictionary_index):
        if self.word_lookup_service.lookup_entry(dictionary_index, word) is not None:
            return True
        return False

    def submit_word(self, word):
        score = 0
        is_valid_word, message = self.evaluate_word(word)
        if is_valid_word:
            self.words_found_list[self.current_player_index].append(word)
            score = self.calculate_score(word)
            self.scores[self.current_player_index] += score
            self.total_scores[self.current_player_index] += score
        return score, self.total_scores[self.current_player_index], message


class SpellingBeeGame(WordGameTemplate):
    MIN_WORD_LEN = 4
    PANGRAM_LEN = 7
    PANGRAM_BONUS = 7
    REQUIRED_LETTER_INDEX = 3

    def __init__(self, word_lookup_service):
        super().__init__(word_lookup_service)
        self.pangram = []

    def register_player(self, username):
        if username not in self.players:
            index = len(self.players)
            self.players.append(username)
            return index
        else:
            return -1

    def setup_game(self):
        for player in self.players:
            self.words_found_list.append([])
            self.scores.append([])
            self.total_scores.append(0)

    def start_game(self):
        print("Calling start_game()")
        pangram = self.get_random_pangram()
        print("Found pangram: " + pangram)
        rand_pangram = self.randomize_word(pangram)
        print("Randomized pangram: " + str(rand_pangram))
        self.pangram = rand_pangram
        return str(self.pangram)

    def end_game(self):
        pass

    def get_random_pangram(self):
        return self.word_lookup_service.get_random_entry_index("pangram_dict")

    def randomize_word(self, word):
        letters = list(set(word))
        shuffle(letters)
        return letters

    def calculate_score(self, word):
        word_len = len(word)
        if word_len == self.MIN_WORD_LEN:
            return 1
        elif self.MIN_WORD_LEN <= word_len < self.PANGRAM_LEN:
            return word_len
        elif word_len >= 7:
            return self.PANGRAM_LEN + self.PANGRAM_BONUS + (word_len - self.PANGRAM_LEN)
        else:
            return 0

    def evaluate_word(self, word):
        if word in self.words_found_list:
            return False, "The word {} has already been found".format(word)

        letters_set = set(word)
        print("Got here")
        pangram_set = set(self.pangram)

        if len(word) < 4 or not letters_set.issubset(pangram_set) or not self.is_in_dictionary(word, "word_dict"):
            return False, "Sorry, that is not a valid word"

        center_letter = self.pangram[self.REQUIRED_LETTER_INDEX]

        if center_letter not in word:
            return False, "Invalid word, missing centre letter {}".format(center_letter)

        if letters_set.issubset(pangram_set):
            if letters_set == self.PANGRAM_LEN:
                return True, "Pangram!"
            else:
                return True, "Valid word"

        return False, "Sorry that is not a valid word"


class SpellingBeeGameBuilder:
    def __init__(self):
        pass

    def __call__(self, dictionaries):
        return SpellingBeeGame(JSONLookupService(source_files_dict=dictionaries))

