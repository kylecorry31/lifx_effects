import time
from utils import sample

class PhasmaHuntEffect:
    def __init__(self, speed):
        self.speed = speed

    def run(self, lights):
        while True:
            speed = sample(self.speed, 40)
            for light in lights:
                light.off(speed)
            time.sleep(speed / 1000.0)
            for light in lights:
                light.on(255, speed)
            time.sleep(speed / 1000.0)