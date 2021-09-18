"""
TCP Server program. Supports multi-threading for connections. Expects messages w/ length and
file type encoded into header

* DEV: Anthony Norderhaug, SDSU Mechatronics
"""
import socket
import pickle
import json
import threading

PORT = 50000
SERVER = 'localhost'
FORMAT = 'utf-8'
DISCONNECT = '!DISCONNECT'
HEADER_SIZE = 64
ADDRESS = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


def start():
    """
    Switches socket into listening mode. Accepts connections & begins thread for handling.
    :return:
    """
    server.listen()
    while True:
        conn, address = server.accept()  # blocking call, waits for incoming connection

        # starts new thread to continue listening
        threading.Thread(target=handle_client, args=(conn, address)).start()
        print(f'| ACTIVE CONNECTIONS: {threading.active_count() - 1} |')  # -1 to ignore server


def encode_length(msg):
    """
    Adds encoded header of 64 bytes (HEADER_SIZE) to msg.
    :param msg:     byte, Message
    :return:        byte, Header and message adjoined
    """
    header = str(len(msg)).encode(FORMAT)

    header += b' ' * (HEADER_SIZE - len(header))
    return header + msg


def decode_length_and_type(conn):
    """
    Returns list of 2 elements containing length & file name. If no file name, '' replaces it
    :param conn:    Socket, the current connection
    :return:        List, 2 elements of msg length and file name
    """
    header = conn.recv(HEADER_SIZE).decode(FORMAT)
    msg_info = header.split('#') if '#' in header else (header, '')

    return msg_info


def handle_message(msg_bytes, name):
    """
    Discerns whether message carries String, serialized object code, or a JSON file
    :param msg_bytes:   byte, Message in byte form
    :param name:        String, file name w/ extension
    :return:            String, console msg stating what was received
    """
    if name == '':
        return msg_bytes.decode(FORMAT)
    else:
        if name[-5:] == '.json':
            json_obj = json.loads(msg_bytes.decode(FORMAT))
            json.dump(json_obj, open('server_' + name, 'w'), indent=2)
        elif name[-7:] == '.pickle':
            pickle_obj = pickle.loads(msg_bytes)
            pickle.dump(pickle_obj, open('server_' + name, 'wb'))
            return f'File "{name}" has been received. | Unpickled: {pickle_obj}'
        else:
            print('File type not recognized.')
        return f'File "{name}" has been received.'


def handle_client(conn, address):
    """
    Program receiving and sending messages to client.
    :param conn:        Socket, current connection
    :param address:     Tuple, contains SERVER and PORT
    :return:
    """
    print(f'{address} Connection accepted!')
    conn.send(encode_length(f'{address} Connection accepted!'.encode(FORMAT)))
    connected = True

    while connected:
        msg_info = decode_length_and_type(conn)  # syntax: length = file_info[0], name = file_info[1]
        msg_bytes = conn.recv(int(msg_info[0]))

        # decides if msg bytes included serialized object or JSON
        message = handle_message(msg_bytes, str(msg_info[1]).strip())
        print(f'{address}: {message}')

        # acknowledgement to client.py
        if message != DISCONNECT:
            conn.send(encode_length("Message received!\n".encode(FORMAT)))
        else:
            connected = False
            conn.send(encode_length("Disconnecting...\n".encode(FORMAT)))

    conn.close()


start()
