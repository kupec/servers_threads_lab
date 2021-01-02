import os
import socket
import yaml

BUFFER_SIZE = 1024
receive_buffer = bytes()
receive_message_queue = []
server_options = []

def write_message(s, message):
    s.send(f'{message}\n'.encode())


def read_message(s):
    global receive_message_queue
    global receive_buffer

    while len(receive_message_queue) == 0:
        chunk = s.recv(BUFFER_SIZE)
        if len(chunk) == 0:
            return None

        receive_buffer += chunk
        messages = receive_buffer.split(b'\n')

        receive_message_queue = messages[0:-1]
        receive_buffer = messages[-1]

    return receive_message_queue.pop(0).decode()


def handle_commands(s):
    while True:
        command = read_message(s)

        if not command:
            break

        if command == 'list':
            write_message(s, ','.join(server_options))
        elif command in server_options:
            os.system('./stop_servers.sh')
            os.system(f'./start_server.sh {command}')
            write_message(s, 'OK')
        else:
            write_message(s, f'Bad command: {command}')


def load_servers_options():
    global server_options

    with open('/servers/docker-compose.yml', 'r') as f:
        config = yaml.load(f, Loader=yaml.Loader)
    server_options = config['services'].keys()


def start():
    load_servers_options()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
        ss.bind(('0.0.0.0', 3000))
        ss.listen()

        try:
            while True:
                s, _ = ss.accept()
                handle_commands(s)
        finally:
            os.system(f'./stop_servers.sh')


if __name__ == '__main__':
    start()
