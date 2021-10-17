from abc import ABC, abstractmethod
from random import shuffle
from services.lookup_service import JSONLookupService


class GameManager(ABC):
    @abstractmethod
    def setup_game(self):
        pass

    @abstractmethod
    def start_game(self):
        pass

    @abstractmethod
    def end_game(self):
        pass


class WordGameTemplate(ABC):
    def __init__(self, word_lookup_service):
        self.word_lookup_service = word_lookup_service
        self.words_found_list = []
        self.scores = []
        self.total_score = 0

    @abstractmethod
    def calculate_word_score(self, word):
        pass

    @abstractmethod
    def evaluate_word(self, word):
        pass

    def is_word_in_dictionary(self, word, dictionary_key):
        if self.word_lookup_service.lookup_entry(dictionary_key, word) is not None:
            return True
        return False

    def check_word(self, word):
        score = 0
        is_valid_word, message = self.evaluate_word(word)
        if is_valid_word:
            self.words_found_list.append(word)
            score = self.calculate_word_score(word)
            self.scores.append(score)
            self.total_score += score
        return score, self.total_score, message


class SpellingBeeGame(WordGameTemplate, GameManager):
    MIN_WORD_LEN = 4
    PANGRAM_LEN = 7
    PANGRAM_BONUS = 7
    REQUIRED_LETTER_INDEX = 3

    def __init__(self, word_lookup_service):
        super().__init__(word_lookup_service)
        self.pangram_letters = []

    def setup_game(self):
        self.words_found_list.clear()
        self.scores.clear()
        self.total_score = 0

    def start_game(self):
        pangram = self.get_random_pangram()
        self.pangram_letters = self.randomize_word(pangram)
        return str(self.pangram_letters)

    def end_game(self):
        pass

    def get_random_pangram(self):
        return self.word_lookup_service.get_random_entry_index("pangram_dict")

    def randomize_word(self, word):
        letters = list(set(word))
        shuffle(letters)
        return letters

    def calculate_word_score(self, word):
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
        if word in self.words_found_list:
            return False, "The word {} has already been found".format(word)

        word_letters_set = set(word)
        pangram_letters_set = set(self.pangram_letters)

        if len(word) < 4 or not word_letters_set.issubset(pangram_letters_set) or \
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


class SpellingBeeGameBuilder:
    def __init__(self):
        pass

    def __call__(self, dictionaries):
        return SpellingBeeGame(JSONLookupService(source_files_dict=dictionaries))

