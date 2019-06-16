from collections import defaultdict

def goes_to(connection, target_in):
    while True:
        if connection.parent.auto_comb:
            connection = connection.parent.o1.connections[0]
        elif connection == target_in:
            return True
        else:
            return False

def disconnect_compound(from_port, to_port):
    while True:
        to_port.disconnect(from_port)
        if to_port.parent.auto_comb:
            # We've found an intermediate operation!
            if to_port.name == 1:
                other_input = to_port.parent.i2
            else:
                other_input = to_port.parent.i1
            other_from = other_input.connections[0]
            if other_from.parent.auto_num:
                # Disconnect everything and keep on deleting.
                other_input.disconnect(other_from)
                from_port = to_port.parent.o1
                to_port = to_port.parent.o1.connections[0]
            else:
                # Delete the operator and patch its other input to its output.
                new_to = to_port.parent.o1.connections[0]
                other_input.disconnect(other_from)
                new_to.disconnect(to_port.parent.o1)
                new_to.connect(other_from)
                break
        else:
            break

class Port:
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.connections = []

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

    def disconnect(self, other):
        self.parent.disconnect(other.parent, self.name, other.name)
        self.connections.remove(other)
        other.connections.remove(self)

    def connect(self, other):
        self.parent.connect(other.parent, self.name, other.name)
        self.connections.append(other)
        other.connections.append(self)


class PortArray:
    def __init__(self, parent):
        self.parent = parent
        self.ports = {}

    @property
    def total_connections(self):
        return sum(len(port.connections) for port in self.ports.values())

    def get(self, name):
        # check name is a valid port name
        pos = int(name[1:])
        try:
            return self.ports[pos]
        except KeyError:
            self.ports[pos] = self.PortClass(self.parent, pos)
            return self.ports[pos]

class InArray(PortArray):
    PortClass = In

class OutArray(PortArray):
    PortClass = Out

class Box:
    def __init__(self, name = "some object", auto_comb=False, auto_num=False):
        self.name = name
        self.auto_comb = auto_comb
        self.auto_num = auto_num
        self.outs = OutArray(self)
        self.ins = InArray(self)

    def connect(self, target, port, target_port):
        pass

    def disconnect(self, target, port, target_port):
        pass

    def make_plusbox(self):
        return Box(name="AutoPlus", auto_comb=True)

    def make_numbox(self, number):
        return Box(name = f"AutoNum {number}", auto_num=True)


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
        return f"Box: {self.name}"


