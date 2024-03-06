class Data:
    def __init__(self, data):
        self.cursor = 0
        self.data = data

    def read(self, count):
        result = self.data[self.cursor: self.cursor + count]
        self.cursor += count
        return result
    
    def move_cursor(self, index):
        self.cursor = index
    
    def show(self):
        return self.data[self.cursor:]