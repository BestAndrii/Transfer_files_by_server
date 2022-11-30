import socket
import pickle

from cryptography.fernet import Fernet


class Client:
    def __init__(self, ip: str, port: int, server_name: str):
        # Создаём соединение
        self.client = socket.socket()
        self.client.connect((ip, port))

        payload = {"type": "CONNECT", "server_name": server_name}
        payload = pickle.dumps(payload)
        self.client.send(payload)

        answer: dict = self.client.recv(1024)
        answer = pickle.loads(answer)
        key: Fernet = answer["key"]

        answer: dict = self.client.recv(1024)
        answer = key.decrypt(answer)
        answer = pickle.loads(answer)

        print(answer)

        with open(answer["file_name"], "w") as file:
            file.write(answer["file_text"])


Client("127.0.0.1", 5555, "ServerName")
