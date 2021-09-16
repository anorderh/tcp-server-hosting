import json
import pickle

class Message:

    def __init__(self, msg, filename=None):
        self.msg = msg
        self.filename = filename
        self.check_file()

    def check_file(self):
        if self.filename is None:
            pass
        elif self.filename[-5:] == '.json':
            print("JSON file recognized.")
            py_json = json.load(open(self.filename, 'r'))
            self.msg = json.dumps(py_json)
        elif self.filename[-7:] == '.pickle':
            print("PICKLE file recognized. ")
            py_pickle = pickle.load(open(self.filename, 'rb'))
            self.msg = pickle.dumps(py_pickle)
        else:
            print("No file type recognized. Defaulting to str.")