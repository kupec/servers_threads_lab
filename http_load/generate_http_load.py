import socket
import os
import subprocess


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
                raise Exception("control server has been shutdown or crashed")

            self.receive_buffer += chunk
            messages = self.receive_buffer.split(b'\n')

            self.receive_message_queue = messages[0:-1]
            self.receive_buffer = messages[-1]

        return self.receive_message_queue.pop(0).decode()


def request_list(socketIO):
    socketIO.write('list')
    servers_message = socketIO.read()
    options = servers_message.split(',')

    yield from options


def filter_with_fzf(option_iter):
    try:
        fzf_process = subprocess.Popen(['fzf'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        for option in option_iter:
            fzf_process.stdin.write(f'{option}\n'.encode())
        fzf_process.stdin.close();

        option = fzf_process.stdout.read().decode().strip()
        code = fzf_process.wait()
        if code == 0:
            return option
    except:
        fzf_process.kill()

    return None


def handle_help_command(socketIO):
    print('\n'.join([
        'list - show servers list and run a selected one',
        'run SERVER - run SERVER and make http load',
        'runall - start `run` command for each server',
        'q/quit - quit',
    ]))


def handle_run_command(server, socketIO):
    socketIO.write(server)
    print(f'Waiting for server {server} starting')
    ready_message = socketIO.read()
    if ready_message == 'OK':
        print(f'Starting load generator for {server}')
        os.system('./hey.sh')
    else:
        print(f'Unknown backend response: {ready_message}')


def handle_list_command(socketIO):
    option = filter_with_fzf(request_list(socketIO))
    if not option:
        return

    handle_run_command(option, socketIO)


def handle_run_all_command(socketIO):
    for server in request_list(socketIO):
        handle_run_command(server, socketIO)


def handle_quit_command(socketIO):
    return True


def handle_commands(socketIO):
    handlers_map = {
        'list': handle_list_command,
        'run': handle_run_command,
        'runall': handle_run_all_command,
        'help': handle_help_command,
        'q': handle_quit_command,
        'quit': handle_quit_command,
    }

    while True:
        command = input('command (or help) > ')
        command_args = command.split(' ')

        handler = handlers_map.get(command_args[0])
        if not handler:
            print('Unknown command, type help')
            continue

        need_exit = handler(*command_args[1:], socketIO=socketIO)
        if need_exit:
            break


def load_env_vars():
    result = {}

    with open('.env', 'r') as f:
        data = f.read()
        for line in data.split('\n'):
            tokens = [x.strip() for x in line.split('=')]
            if len(tokens) == 2:
                key, value = tokens
                result[key] = value

    return result


def start():
    envs = load_env_vars()
    host = envs['HOST']

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, 3000))
        handle_commands(SocketIO(s))


if __name__ == '__main__':
    start()
