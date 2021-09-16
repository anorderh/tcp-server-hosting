import socket
import pickle
import json
import pathlib
import messages
import Car
import threading

PORT = 50000
SERVER = socket.gethostbyname(socket.gethostname())
HEADER = 16
FORMAT = 'utf-8'
DISCONNECT = '!DISCONNECT'
ADDRESS = (SERVER, PORT)
HEADER_SIZE = 64


def encode_length(msg):
    header = str(len(msg)).encode(FORMAT)

    header += b' ' * (HEADER_SIZE - len(header))
    return header + msg


def decode_length():
    return int(client.recv(HEADER_SIZE).decode(FORMAT))


def check(user_input):
    file_ext = pathlib.PurePath(user_input).suffix
    if file_ext != '':
        return messages.Message(user_input, user_input)
    else:
        return messages.Message(user_input)


def receive():
    msg = pickle.loads(client.recv(decode_length()))
    print(f'{ADDRESS}: {msg}')

    if msg == 'Disconnecting...':
        return False
    else:
        return True


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDRESS)

    while receive():
        print("Send either a file or message.")
        message_OBJ = check(input())
        client.send(encode_length(pickle.dumps(message_OBJ)))

    client.close()

    # # test 1: sending an int
    # client.send(str(453).encode(FORMAT))
    # print(client.recv(1024).decode(FORMAT))
    #
    # # test 2: sending a str
    # client.send('Hi server, how is your day going?'.encode(FORMAT))
    # print(client.recv(1024).decode(FORMAT))
    #
    # # test 3: sending Object file in pickled byte representation
    # pickle_bytes = pickle.dumps(Car('2015', 'grey', 'civic'))
    # client.send(pickle_bytes)
    #
    # # test 4: creating json obj, then dumping obj into str, then sending string encoded
    # json_obj = json.load(open('sample.json', 'r'))
    # json_string = json.dumps(json_obj)
    # client.send(json_string.encode(FORMAT))
