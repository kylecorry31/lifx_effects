import time
from utils import rand

class CandleEffect:

    def __init__(self, speed, amount):
        self.speed = speed
        self.amount = amount

    def run(self, lights):
        while True:
            for light in lights:
                light.on(255 - self.amount / 100 * 255 + rand(0, self.amount), self.speed)
            time.sleep(self.speed / 1000.0)