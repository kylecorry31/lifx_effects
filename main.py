from utils.lights import get_lights
from effects.candle_effect import CandleEffect
from effects.phasma_hunt_effect import PhasmaHuntEffect
from effects.wav_effect import WavEffect
from effects.midi_effect import MidiEffect

lights = get_lights(2)

try:
    # PhasmaHuntEffect(250).run(lights)
    # CandleEffect(250, 45).run(lights)
    MidiEffect('music/2.mid', [0, 0], 2).run(lights)
    # MidiEffect('music/4.mid', [2, 6], 2).run(lights)
    # WavEffect("music/4.wav", 2, 0.01).run(lights)
except:
    for light in lights:
        light.on(255)