
class Area:
    def __init__(self, start_row, finish_row):
        self.start_row = start_row
        self.finish_row = finish_row
        self.x = 1
        self.y = start_row

    def get_next_space(self):
        x, y = self.x, self.y
        if self.y + 1 > self.finish_row:
            self.x += 1
            self.y = self.start_row
        else:
            self.y += 1
        return x * 50, y * 50

class Canvas:
    def __init__(self, name):
        self.name = name
        self.boxes = []
        self.connections = []
        self.areas = {"inlet" : Area(1, 1),
                      "main" : Area(2, 6),
                      "outlet" : Area(7, 7)}

    def box_id(self, box):
        return self.box_number(box) + 1


    def box_number(self, box):
        try:
            return self.boxes.index(box)
        except ValueError:
            return -1

    def get_new_location(self, box_type = "main"):
        return self.areas[box_type].get_next_space()

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

