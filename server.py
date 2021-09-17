import socket
import pickle
import json
import threading

PORT = 50000
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCONNECT = '!DISCONNECT'
HEADER_SIZE = 64

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))


def start():
    server.listen()
    while True:
        conn, address = server.accept()  # blocking call, waits for incoming connection

        # starts new thread to continue listening
        threading.Thread(target=handle_client, args=(conn, address)).start()
        print(f'| ACTIVE CONNECTIONS: {threading.active_count() - 1} |')  # -1 to ignore server


def encode_length(msg):
    header = str(len(msg)).encode(FORMAT)

    header += b' ' * (HEADER_SIZE - len(header))
    return header + msg


def decode_length_and_type(conn):
    header = conn.recv(HEADER_SIZE).decode(FORMAT)
    msg_info = header.split('#') if '#' in header else (header, '')

    return msg_info


def handle_message(msg_bytes, name):
    if name == '':
        return msg_bytes.decode(FORMAT)
    else:
        if name[-5:] == '.json':
            json_obj = json.loads(msg_bytes.decode(FORMAT))
            json.dump(json_obj, open('server_' + name, 'w'), indent=2)
        elif name[-7:] == '.pickle':
            pickle_obj = pickle.loads(msg_bytes)
            return f'Object "{name}" has been received. | Unpickled: {pickle_obj}'
        else:
            print('File type not recognized.')
        return f'File "{name}" has been received.'


def handle_client(conn, address):
    print(f'{address} Connection accepted!')  # confirms accept
    conn.send(encode_length(f'{address} Connection accepted!'.encode(FORMAT)))
    connected = True

    while connected:
        msg_info = decode_length_and_type(conn)  # syntax: length = file_info[0], name = file_info[1]
        msg_bytes = conn.recv(int(msg_info[0]))  # in bytes form

        message = handle_message(msg_bytes, str(msg_info[1]).strip())
        print(f'{address}: {message}')

        if message != DISCONNECT:
            conn.send(encode_length("Message received!\n".encode(FORMAT)))
        else:
            connected = False
            conn.send(encode_length("Disconnecting...\n".encode(FORMAT)))

    conn.close()


start()
