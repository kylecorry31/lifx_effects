from utils.lights import get_lights
from effects.candle_effect import CandleEffect
from effects.phasma_hunt_effect import PhasmaHuntEffect

lights = get_lights(2)

try:
    # PhasmaHuntEffect(250).run([left, right])
    CandleEffect(250, 45).run(lights)
except:
    for light in lights:
        light.on(255)