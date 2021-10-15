import logging

import grpc

import word_game_pb2
import word_game_pb2_grpc


def run():
    channel = grpc.insecure_channel('127.0.0.1:50055')
    stub = word_game_pb2_grpc.WordGameStub(channel)

    game_id = stub.CreateGame(word_game_pb2.GameRequest(gameType="SpellingBee")).gameId
    player_index = stub.RegisterPlayer(word_game_pb2.RegisterRequest(gameId=game_id, playerName="test")).playerIndex
    letters = stub.InitGameRequest(word_game_pb2.InitRequest(gameId=game_id)).letters
    print("Letters: " + letters)
    submission_response = stub.SubmitWord(word_game_pb2.WordSubmissionRequest(playerIndex=player_index, gameId=game_id,
                                                                              word="blabla"))

    print("Score: " + str(submission_response.score))
    print("Total: " + str(submission_response.total))
    print("Message: " + str(submission_response.message))


if __name__ == '__main__':
    logging.basicConfig()
    run()
