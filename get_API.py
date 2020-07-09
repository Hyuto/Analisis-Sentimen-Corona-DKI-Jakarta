class API(object):
    def __init__(self, text = "API.txt"):
        f = open(text, 'r')
        data = f.readlines()
        f.close()
        for i in range(4):
            start = data[i].index('"')
            stop = start + data[i][start+1:].index('"') + 1
            data[i] = data[i][start+1:stop]
        self.data = data

    def get(self):
        return self.data[:4]