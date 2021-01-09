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


def handle_help_command(socketIO, **kwargs):
    print('\n'.join([
        'list - show servers list and run a selected one',
        'run SERVER - run SERVER and make http load',
        'runall - start `run` command for each server',
        'q/quit - quit',
    ]))


def open_log_destination(server, **kwargs):
    log_path = os.getenv('LOG_FILE').format(server)
    return open(log_path, 'w')


def run_load_generator(server):
    concurrency = os.getenv('CONCURRENCY')
    request_timeout = os.getenv('REQUEST_TIMEOUT')
    total_timeout = os.getenv('TOTAL_TIMEOUT')
    host = os.getenv('HOST')

    with open_log_destination(server) as log_file:
        subprocess.run(
            [
                'hey',
                '-c', concurrency,
                '-t', request_timeout,
                '-z', f'{total_timeout}s',
                f'http://{host}:3001',
            ],
            stdout=log_file
        )


def handle_run_command(server, /, socketIO, **kwargs):
    socketIO.write(server)
    print(f'Waiting for server {server} starting')
    ready_message = socketIO.read()
    if ready_message == 'OK':
        print(f'Starting load generator for {server}')
        run_load_generator(server)
    else:
        print(f'Unknown backend response: {ready_message}')


def handle_list_command(socketIO, **kwargs):
    option = filter_with_fzf(request_list(socketIO))
    if not option:
        return

    handle_run_command(option, socketIO=socketIO, **kwargs)


def handle_run_all_command(socketIO, **kwargs):
    for server in request_list(socketIO):
        handle_run_command(server, socketIO, **kwargs)


def handle_quit_command(socketIO, **kwargs):
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


def start():
    host = os.getenv('HOST')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, 3000))
        handle_commands(SocketIO(s))


if __name__ == '__main__':
    start()
