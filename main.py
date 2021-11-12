from effects.keyboard_effect import KeyboardEffect
from utils.lights import get_lights
from effects.candle_effect import CandleEffect
from effects.phasma_hunt_effect import PhasmaHuntEffect
from effects.audio_spectrum_effect import AudioSpectrumEffect
from effects.audio_amplitude_effect import AudioAmplitudeEffect
from effects.midi_effect import MidiEffect
import time

lights = get_lights(3)

try:
    # PhasmaHuntEffect(250).run(lights)
    # CandleEffect(250, 45).run(lights)
    # KeyboardEffect(['a', 'd'], 200).run(lights)
    # MidiEffect('music/2.mid', [0, 0], 2).run(lights)
    # MidiEffect('music/6.mid', [4, 9], 1, True).run(lights)
    # AudioSpectrumEffect("music/1.wav", 1, bins=[2, 2], num_bins=1024).run(lights)
    # AudioSpectrumEffect("music/2.wav", 1, bins=[14, 15, 16], num_bins=1024).run(lights)
    AudioAmplitudeEffect("microphone", 3).run(lights)
finally:
    time.sleep(0.2)
    for light in lights:
        light.on(255)
    time.sleep(1)
    for light in lights:
        light.on(255)