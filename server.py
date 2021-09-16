import socket
import pickle
import json
import threading

PORT = 50000
SERVER = socket.gethostbyname(socket.gethostname())
HEADER = 16
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


def decode_length(conn):
    return int(conn.recv(HEADER_SIZE).decode(FORMAT))


def handle_file(msg):
    if msg.filename is not None:
        if msg.filename[-5:] == '.json':
            json.dump(msg.msg, open('server_' + msg.filename, 'w'), indent=2)
        elif msg.filename[-7:] == '.pickle':
            pickle.dump(msg.msg, open('server_' + msg.filename, 'wb'))
        msg.msg = msg.filename


def handle_client(conn, address):
    print(f'{address} Connection accepted!')  # confirms accept
    conn.send(encode_length(pickle.dumps(f'{address} Connection accepted!')))
    connected = True

    while connected:
        # retrieves msg & checks for files
        msg = pickle.loads(conn.recv(decode_length(conn)))
        handle_file(msg)
        conn.send(encode_length(pickle.dumps("Message received!")))
        print(f'{address}: {msg.msg}')

        if str(msg.msg) == DISCONNECT:
            connected = False
            conn.send(encode_length(pickle.dumps("Disconnecting...")))

    conn.close()


start()
