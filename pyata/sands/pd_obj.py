from .api import Box
import sands.box_classes.box as box
import sands.box_classes.canvas as canvas
from sands.box_classes.object import Object
from sands.box_classes.number import Number
from sands.box_classes.message import Message
from sands.box_classes.connection import connect, disconnect

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
        x, y = canvas.current.get_new_location()
        self.obj = Object(x, y, text)

class SubPatch(PdBox):
    def __init__(self, name, func):
        super(SubPatch, self).__init__(name)
        x, y = canvas.current.get_new_location()
        self.obj = Object(x, y, "pd " + name)
        canvas.set_current("pd-" + name)
        print(f"moved to {canvas.current.name}")
        func()
        canvas.set_current()

class PdMess(PdBox):
    def __init__(self, message):
        super(PdMess, self).__init__(f"Message: {message}")
        x, y = canvas.current.get_new_location()
        self.obj = Message(x, y, message)

    def click(self):
        self.obj.click()

class PdNum(PdBox):
    def __init__(self, number):
        super(PdNum, self).__init__(f"Number: {number}")
        x, y = canvas.current.get_new_location()
        self.obj = Number(x, y)
        self.obj.set(number)

    def set(self, value):
        self.obj.set(value)

