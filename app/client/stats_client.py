import socket
import json

HOSTNAME = "localhost"
PORT = 65512

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOSTNAME, PORT))
    while True:
        data = sock.recv(4098)
        if data is not None:
            stats = json.loads(data)
            print(stats)
