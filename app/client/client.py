import logging

import grpc

import word_game_pb2
import word_game_pb2_grpc


class Client:
    game_type = "SpellingBee"
    game_loop = True

    def __init__(self):
        print("Spelling Bee!")
        self.channel = grpc.insecure_channel('127.0.0.1:50055')
        self.stub = word_game_pb2_grpc.WordGameStub(self.channel)
        self.game_id = self.stub.CreateGame(word_game_pb2.GameRequest(gameType=self.game_type)).gameId
        self.letters = self.stub.InitGameRequest(word_game_pb2.InitRequest(gameId=self.game_id)).letters

    def run(self):
        while self.game_loop:
            print(self.letters)
            word = input("Enter a word: ")
            response = self.stub.SubmitWord(word_game_pb2.WordSubmissionRequest(gameId=self.game_id, word=word.lower()))
            print(response.message, "- Score:", response.score, "Total:", response.total)


if __name__ == '__main__':
    logging.basicConfig()
    client = Client()
    client.run()

