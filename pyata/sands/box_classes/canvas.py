


class Canvas:
    def __init__(self, name):
        self.name = name
        self.boxes = []
        self.connections = []
        self.next_x = 1
        self.next_y = 1

    def box_id(self, box):
        return self.box_number(box) + 1


    def box_number(self, box):
        try:
            return self.boxes.index(box)
        except ValueError:
            return -1

    def get_new_location(self):
        if self.next_y < 8:
            self.next_y += 1
        else:
            self.next_y = 1
            self.next_x += 1
        return self.next_x * 100, self.next_y * 100


    def clear(self):
        self.boxes = []
        self.connections = []

canvas_lookup = {"pd-new" : Canvas("pd-new")}


current = canvas_lookup["pd-new"] 

def set_current(name = None):
    global current
    print(current.name)
    name = name or "pd-new"
    try:
        current = canvas_lookup[name]
    except KeyError:
        current = Canvas(name)
        canvas_lookup[name] = current
    print("set", current.name)

