from lifxlan import LifxLAN

def get_lights(count):
    lifx = LifxLAN(count)
    lights = lifx.get_lights()
    return [Light(light) for light in lights]

class Light:
    def __init__(self, light, max_brightness=255):
        self.light = light
        self.last_time = 0
        self.max_brightness = max_brightness

    def off(self, duration = 0):
        self.on(0, duration)

    def on(self, power=255, duration = 0):
        self.light.set_brightness(
            max(0, min(self.max_brightness, power) * 257), duration, True)