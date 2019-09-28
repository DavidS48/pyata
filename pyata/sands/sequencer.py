
import time


class Stopped(Exception):
    pass

class ValueChannel:
    def __init__(self, values, targets = None):
        self.values = values
        self.targets = targets or []

    def play(self, position):
        try:
            value = self.values[position]
            for target in self.targets:
                target.set(value)
        except KeyError:
            pass

class ValueSequencer:
    def __init__(
            self,
            bpm,
            pattern,
            div=4,
            value_targets = None,
            bang_targets = None):
        self.bpm = bpm
        self.div = div
        self.length = len(pattern)
        self.channels = [ValueChannel(pattern, value_targets)]
        self.bang_targets = bang_targets or []
        self.infinite = True
        self.current_pos = 0

    def run(self):
        start_time = time.time()
        while True:
            try:
                div_time = 60 / (self.div * self.bpm)
                self._tick()
                time.sleep(div_time + start_time - time.time())
                start_time += div_time
            except Stopped:
                break

    def add_channel(self, pattern, targets):
        self.channels.append(ValueChannel(pattern, targets))


    def _tick(self):
        for channel in self.channels:
            channel.play(self.current_pos)
        for target in self.bang_targets:
            target.click()
        self.current_pos += 1
        if self.current_pos >= self.length:
            if self.infinite:
                self.current_pos = 0
            else:
                raise Stopped()


