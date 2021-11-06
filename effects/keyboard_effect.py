import time
import keyboard

class KeyboardEffect:

    def __init__(self, keys, ramp_time = 0):
        self.keys = keys
        self.was_pressed = [False for _ in keys]
        self.ramp_time = ramp_time

    def run(self, lights):
        for light in lights:
            light.off()
        while True:
            for i in range(0, len(self.keys)):
                pressed = keyboard.is_pressed(self.keys[i])
                if pressed and not self.was_pressed[i]:
                    try:
                        lights[i].on(duration = self.ramp_time)
                        self.was_pressed[i] = True
                    except:
                        pass
                elif not pressed and self.was_pressed[i]:
                    try:
                        lights[i].off(duration = self.ramp_time)
                        self.was_pressed[i] = False
                    except:
                        pass