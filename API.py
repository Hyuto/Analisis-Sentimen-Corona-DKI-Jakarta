import json

class API(object):
    def __init__(self, text = "API.json"):
        with open(text, 'r') as f:
            self.data = json.load(f)