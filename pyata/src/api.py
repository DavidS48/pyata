from collections import defaultdict

def goes_to(connection, target_in):
    while True:
        if type(connection.parent) == AutoComb:
            connection = connection.parent.o1.connections[0]
        elif connection == target_in:
            return True
        else:
            return False

def disconnect(output, connection):
    while True:
        if type(connection.parent) == AutoComb:
            # We've found an intermediate operation!
            if connection.name == "i1":
                other_input = connection.parent.i2
            else:
                other_input = connection.parent.i1
            other_source = other_input.connections[0]
            if type(other_source.parent) == AutoNum:
                # Delete the operator and its other input and carry on down.
                output = connection.parent.o1
                connection = connection.parent.o1.connections[0]
            else:
                # Delete the operator and patch its other input to its output.
                output = connection.parent.o1
                other_source._replace(other_input, connection.parent.o1.connections[0])
                connection.parent.o1.connections[0]._replace(output, other_source)
                break
        else:
            connection._remove(output)
            break


class Out:
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.connections = []

    def _remove(self, other):
        self.connections = [c for c in self.connections if c != other]

    def _replace(self, old_other, new_other):
        self.connections = [c if c != old_other else new_other for c in self.connections]

    def __ror__(self, other):
        if type(other) == In:
            new_self_connections = []
            for c in self.connections:
                if goes_to(c, other):
                    disconnect(self, c)
                else:
                    new_self_connections.append(c)
            self.connections = new_self_connections
        else:
            raise TypeError

    def __add__(self, other):
        if type(other) == Out:
            plusbox = AutoComb("+")
            plusbox.i1 << self
            plusbox.i2 << other
            return plusbox.o1
        elif type(other) in (float, int):
            numbox = AutoNum(str(other))
            plusbox = AutoComb("+")
            plusbox.i1 << self
            plusbox.i2 << numbox.o1
            return plusbox.o1
        else:
            raise TypeError


    def __repr__(self):
        return f"{self.parent}.{self.name}"

class In:
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.connections = []

    def _remove(self, other):
        self.connections = [c for c in self.connections if c != other]

    def _replace(self, old_other, new_other):
        self.connections = [c if c != old_other else new_other for c in self.connections]

    def __repr__(self):
        return f"{self.parent}.{self.name}"

    def __lshift__(self, other):
        if type(other) == Out:
            self.connections.append(other)
            other.connections.append(self)
        else:
            raise TypeError

    def __ilshift__(self, other):
        if type(other) == Out:
            if self.connections:
                self.connections[-1] = other
            else:
                self.connections = [other]
            other.connections.append(self)
        else:
            raise TypeError

    def __ror__(self, other):
        if type(other) == Out:
            new_other_connections = []
            for c in other.connections:
                if goes_to(c, self):
                    disconnect(other, c)
                else:
                    new_other_connections.append(c)
            other.connections = new_other_connections
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
    def __init__(self, name = "some object"):
        self.name = name
        self.outs = OutArray(self)
        self.ins = InArray(self)

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

class AutoComb(Obj):
    def __repr__(self):
        return f"AutoComb: {self.name}"

class AutoNum(Obj):
    def __repr__(self):
        return f"AutoNum: {self.name}"


