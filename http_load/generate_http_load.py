import socket
import os
import subprocess

BUFFER_SIZE = 1024
receive_buffer = bytes()
receive_message_queue = []

def read_message(s):
    global receive_message_queue
    global receive_buffer

    while len(receive_message_queue) == 0:
        chunk = s.recv(BUFFER_SIZE)
        if len(chunk) == 0:
            raise Exception("control server has been shutdown or crashed")

        receive_buffer += chunk
        messages = receive_buffer.split(b'\n')

        receive_message_queue = messages[0:-1]
        receive_buffer = messages[-1]

    return receive_message_queue.pop(0).decode()


def request_list(s):
    s.send(b'list\n')
    servers_message = read_message(s)
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


def handle_commands(s):
    while True:
        option = filter_with_fzf(request_list(s))
        if not option:
            break

        s.send(f'{option}\n'.encode())
        ready_message =  read_message(s)
        if ready_message != 'OK':
            print(f'Unknown response: {ready_message}')
            continue

        os.system('./hey.sh')


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
        handle_commands(s)


if __name__ == '__main__':
    start()
