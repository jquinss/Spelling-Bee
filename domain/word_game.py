from abc import ABC, abstractmethod
from random import shuffle

class WordGameTemplate(ABC):
    def __init__(self, word_lookup_service):
        self.word_lookup_service = word_lookup_service
        self.players = []
        self.scores = []
        self.total_scores = []
        self.current_player_index = -1

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
            score = self.calculate_score(word)
            self.total_scores[self.current_player_index] += score
        return score, self.total_scores[self.current_player_index], message


class SpellingBeeGame(WordGameTemplate):
    MIN_WORD_LEN = 4
    PANGRAM_LEN = 7
    PANGRAM_BONUS = 7
    REQUIRED_LETTER_INDEX = 3

    def __init__(self, word_lookup_service):
        super().__init__(word_lookup_service)
        self.words_found_list = []
        self.pangram = self.randomize_word(self.get_random_pangram())

    def get_random_pangram(self):
        return self.word_lookup_service.get_random_entry_index("pangram_dict")

    def randomize_word(self, word):
        return shuffle(list(word))

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



