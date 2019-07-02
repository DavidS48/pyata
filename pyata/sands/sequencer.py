
import time


class ValueSequencer:
    def __init__(
            self,
            bpm,
            pattern,
            div=4,
            value_targets = None,
            bang_targets = None):
        self.bpm = bpm
        self.pattern = pattern
        self.div = div
        self.value_targets = value_targets or []
        self.bang_targets = bang_targets or []
        self.infinite = True

    def run(self):
        start_time = time.time()
        value_iter = iter(self.pattern)
        while True:
            div_time = 60 / (self.div * self.bpm)
            try:
                value = next(value_iter)
            except StopIteration:
                if self.infinite:
                    value_iter = iter(self.pattern)
                    value = next(value_iter)
                else:
                    break
            for target in self.value_targets:
                target.set(value)
            for target in self.bang_targets:
                target.click()
            time.sleep(div_time + start_time - time.time())
            start_time += div_time


