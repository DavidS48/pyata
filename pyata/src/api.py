from collections import defaultdict

def goes_to(connection, target_in):
    while True:
        if connection.parent.auto:
            connection = connection.parent.o1.connections[0]
        elif connection == target_in:
            return True
        else:
            return False

def disconnect_compound(from_port, to_port):
    while True:
        from_port.disconnect(to_port)
        if to_port.parent.auto:
            # We've found an intermediate operation!
            if to_port.name == "i1":
                other_input = to_port.parent.i2
            else:
                other_input = to_port.parent.i1
            other_from = other_input.connections[0]
            if other_from.parent.auto: # need to check it's a number
                # Have to hope it gets deleted when it has no connections.
                other_from.disconnect(other_input)
                from_port = to_port.parent.o1
                to_port = to_port.parent.o1.connections[0]
            else:
                # Delete the operator and patch its other input to its output.
                new_to = to_port.parent.o1.connections[0]
                other_input.disconnect(other_from)
                to_port.parent.o1.disconnect(new_to)
                other_from.connect(new_to)
                break
        else:
            break

class Port:
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.connections = []

    def disconnect(self, other):
        self.connections.remove(other)
        other.connections.remove(self)

    def connect(self, other):
        self.connections.append(other)
        other.connections.append(self)

class Out(Port):

    def __add__(self, other):
        if type(other) == Out:
            plusbox = self.parent.make_plusbox()
            plusbox.i1 << self
            plusbox.i2 << other
            return plusbox.o1
        elif type(other) in (float, int):
            numbox = self.parent.make_numbox(str(other))
            plusbox = self.parent.make_plusbox()
            plusbox.i1 << self
            plusbox.i2 << numbox.o1
            return plusbox.o1
        else:
            raise TypeError

    def __ror__(self, other):
        if type(other) == In:
            return self | other
        else:
            raise TypeError

    def __repr__(self):
        return f"{self.parent}.{self.name}"

class In(Port):
    def __repr__(self):
        return f"{self.parent}.{self.name}"

    def __lshift__(self, other):
        if type(other) == Out:
            self.connect(other)
        else:
            raise TypeError

    def __ilshift__(self, other):
        if type(other) == Out:
            if self.connections:
                self | self.connections[-1]
            self << other
        else:
            raise NotImplementedError

    def __ror__(self, other):
        if type(other) == Out:
            for c in other.connections:
                if goes_to(c, self):
                    disconnect_compound(other, c)
        else:
            raise TypeError


class PortArray:
    def __init__(self, parent):
        self.parent = parent
        self.ports = {}

    @property
    def total_connections(self):
        return sum(len(port.connections) for port in self.ports.values())

    def get(self, name):
        try:
            return self.ports[name]
        except KeyError:
            self.ports[name] = self.PortClass(self.parent, name)
            return self.ports[name]

class InArray(PortArray):
    PortClass = In

class OutArray(PortArray):
    PortClass = Out

class Obj:
    def __init__(self, name = "some object", auto=False):
        self.name = name
        self.auto = auto
        self.outs = OutArray(self)
        self.ins = InArray(self)

    def make_plusbox(self):
        return Obj(name="AutoPlus", auto=True)

    def make_numbox(self, number):
        return Obj(name = f"AutoNum {number}", auto=True)


    def __getattr__(self, name):
        if name.startswith("i"):
            return self.ins.get(name)
        elif name.startswith("o"):
            return self.outs.get(name)
        else:
            raise AttributeError

    def show_outputs(self):
        for key, value in self.outs.ports.items():
            if value.connections:
                print(key, "->", value.connections)

    def show_inputs(self):
        for key, value in self.ins.ports.items():
            if value.connections:
                print(value.connections, "->", key)

    def __repr__(self):
        return f"Object: {self.name}"


