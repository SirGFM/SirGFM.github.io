
class Defer:
    def __init__(self):
        self.callbacks = []

    def push(self, callback):
        self.callbacks.append(callback)

    def run(self):
        while len(self.callbacks) > 0:
            self.callbacks.pop()()

