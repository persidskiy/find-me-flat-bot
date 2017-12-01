import json
from datetime import datetime
import os.path


def log(message):
    print "[{}] {}".format(str(datetime.now()), message)

def load_json(fname, default_value):
    if not os.path.isfile(fname):
        return default_value
    with open(fname, "r") as fp:
        try:
            data = json.load(fp)
        except ValueError:
            data = default_value
        return data


def save_json(fname, data):
    with open(fname, "w") as fp:
        json.dump(data, fp)
