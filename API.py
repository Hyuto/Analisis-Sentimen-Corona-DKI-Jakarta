import json

class API(object):
    """ Load & Preprocess API.json """
    def __init__(self, text):
        with open(text, 'r') as f:
            self.data = json.load(f)