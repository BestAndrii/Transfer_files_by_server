import socket
import pickle

from loguru import logger

from cryptography.fernet import Fernet


with open("file.txt") as file:
    file_text = file.read()


@logger.catch()
class Server:
    def __init__(self, ip: str,
                 port: int,
                 server_name: str,
                 file_name: str):
        self.server_name = server_name
        self.file_name = file_name

        # Создаём сервер
        self.server = socket.socket()
        self.server.bind((ip, port))
        self.server.listen(0)

        # Генерируем ключ шифрования
        self.key = Fernet(Fernet.generate_key())

        # Запускаем прослушку соиденений
        self.connect_handler()

    def connect_handler(self):
        while True:
            user, adress = self.server.accept()

            # Получаем ответ клиента
            ans = pickle.loads(user.recv(1024))

            # Если это запрос на подключение
            if ans["type"] == "CONNECT":
                if ans["server_name"] == self.server_name:
                    key = {"key": self.key}
                    key = pickle.dumps(key)
                    user.send(key)

                    file = {"file_name": self.file_name,
                            "file_text": file_text}
                    file = self.key.encrypt(pickle.dumps(file))

                    user.send(file)


if __name__ == "__main__":
    Server("127.0.0.1", 5555, "ServerName", "file.txt")
