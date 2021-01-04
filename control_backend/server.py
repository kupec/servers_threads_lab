import os
import socket
import yaml
from pydantic import BaseModel


class Settings(BaseModel):
    HOST: str = '0.0.0.0'
    PORT: int = 3000
    SERVERS_PATH: str = '../servers'


class SocketIO:
    BUFFER_SIZE = 1024

    def __init__(self, s):
        self.s = s
        self.receive_buffer = bytes()
        self.receive_message_queue = []

    def write(self, message):
        self.s.send(f'{message}\n'.encode())

    def read(self):
        while len(self.receive_message_queue) == 0:
            chunk = self.s.recv(self.BUFFER_SIZE)
            if len(chunk) == 0:
                return None

            self.receive_buffer += chunk
            messages = self.receive_buffer.split(b'\n')

            self.receive_message_queue = messages[0:-1]
            self.receive_buffer = messages[-1]

        return self.receive_message_queue.pop(0).decode()


def handle_commands(socketIO, / , server_options, settings):
    while True:
        command = socketIO.read()

        if not command:
            break

        if command == 'list':
            socketIO.write(','.join(server_options))
        elif command in server_options:
            os.system('./stop_servers.sh')
            os.system(f'./start_server.sh {command}')
            socketIO.write('OK')
        else:
            socketIO.write(f'Bad command: {command}')


def load_servers_options(settings: Settings):
    docker_compose_path = os.path.join(settings.SERVERS_PATH, 'docker-compose.yml')
    with open(docker_compose_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.Loader)
    return config['services'].keys()


def start():
    settings = Settings(**os.environ)
    server_options = load_servers_options(settings)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
        ss.bind((settings.HOST, settings.PORT))
        ss.listen()

        try:
            while True:
                s, _ = ss.accept()
                with s:
                    handle_commands(SocketIO(s), server_options=server_options, settings=settings)
        finally:
            os.system(f'./stop_servers.sh')


if __name__ == '__main__':
    start()
