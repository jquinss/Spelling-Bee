from abc import ABC, abstractmethod

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

    def lookup_word(self, word, **kwargs):
        if self.word_lookup_service.is_valid(word, **kwargs):
            return True
        return False

    def submit_word(self, word):
        score = 0
        is_valid_word, message = self.evaluate_word(word)
        if is_valid_word:
            score = self.calculate_score(word)
            self.total_scores[self.current_player_index] += score
        return score, self.total_scores[self.current_player_index], message
