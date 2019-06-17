from .api import Box
from .Pd import Object, Number, connect, disconnect

class LocationMap:
    def __init__(self):
        self.x = 0
        self.y = 0

    def get_new_location(self):
        if self.y < 20:
            self.y += 1
        else:
            self.y = 1
            self.y += 1
        return self.x * 100, self.y * 100

locations = LocationMap()

class PdBox(Box):
    def connect(self, source, port, source_port):
        connect(source.obj, source_port, self.obj, port)

    def disconnect(self, source, port, source_port):
        disconnect(source.obj, source_port, self.obj, port)

    def move(self, x, y):
        print("Moving ", self, x, y)
        self.obj.move(x, y)

    def make_plusbox(self):
        return PdObj("+~")

    def make_multbox(self):
        return PdObj("*~")

    def make_numbox(self, number):
        return PdNum(number)

class PdObj(PdBox):
    def __init__(self, text):
        super(PdObj, self).__init__(text)
        x, y = locations.get_new_location()
        self.obj = Object(x, y, text)

class PdNum(PdBox):
    def __init__(self, number):
        super(PdNum, self).__init__(f"Number: {number}")
        x, y = locations.get_new_location()
        self.obj = Number(x, y)
        self.obj.set(number)

    def set(self, value):
        self.obj.set(value)
