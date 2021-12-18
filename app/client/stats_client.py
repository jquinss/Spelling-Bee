import socket
import json

HOSTNAME = "127.0.0.1"
PORT = 65512


def print_stats(stats):
    pangram = stats["pangram"]
    print(f"Pangram: {pangram}")
    print("Players:")
    for player in stats["players"]:
        player_stats = stats["players"][player]
        total = player_stats["total"]
        words = player_stats["words"]
        print(f"Username: {player}, Total score: {total}, Words found: {words},")
    word_scores = stats["words_found"]
    print(f"Scores per word: {word_scores}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOSTNAME, PORT))
    print("Connected to the stats server. Waiting for stats...")
    while True:
        data = sock.recv(4098)
        if data is not None:
            stats = json.loads(data)
            print_stats(stats)


