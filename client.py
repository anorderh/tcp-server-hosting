import socket
import pickle
import json
import pathlib
import Car

PORT = 50000
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCONNECT = '!DISCONNECT'
ADDRESS = (SERVER, PORT)
HEADER_SIZE = 64


def encode_length_and_type(msg):
    file_name = ''
    file_ext = pathlib.PurePath(str(msg)).suffix

    if file_ext != '':
        file_name = msg
        if file_ext == '.json':
            py_json = json.load(open(file_name, 'r'))
            msg = json.dumps(py_json).encode(FORMAT)
        elif file_ext == '.pickle':
            py_pickle = pickle.load(open(file_name, 'rb'))
            msg = pickle.dumps(py_pickle)
    else:
        msg = str(msg).encode(FORMAT)

    header = str(len(msg)).encode(FORMAT)
    if file_name != '':
        header += ('#' + file_name).encode(FORMAT)

    header += b' ' * (HEADER_SIZE - len(header))
    return header + msg


def decode_length():
    return int(client.recv(HEADER_SIZE).decode(FORMAT))


def receive():
    msg = client.recv(decode_length()).decode(FORMAT)
    print(f'{ADDRESS}: {msg}')


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDRESS)
    receive()

    test = [1, "Hi server!", 'new_car.pickle', 'sample.json']

    print("TEST CASE #1: Sending an int")
    input()
    client.send(encode_length_and_type(test[0]))
    receive()

    print("TEST CASE #2: Sending a str")
    input()
    client.send(encode_length_and_type(test[1]))
    receive()

    print("TEST CASE #3: Sending an object serialized in pickle file")
    input()
    pickle.dump(Car.Car('2015', 'grey', 'civic'), open(test[2], 'wb'))  # generating pickle file
    client.send(encode_length_and_type(test[2]))
    receive()

    print("TEST CASE #4: Sending JSON")
    input()
    client.send(encode_length_and_type(test[3]))    # pre-existing json file
    receive()

    print("Testing DISCONNECT message")
    input()
    client.send(encode_length_and_type(DISCONNECT))     # disconnecting
    receive()

    client.close()
