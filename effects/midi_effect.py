import mido
import pygame
import pygame.midi
import time
import threading

print_all = False
print_instruments = False

class _MidiNote:

    def __init__(self, msg):
        d = msg.dict()
        self.note = d['note']
        self.channel = d['channel']
        self.velocity = d['velocity']
        self.on = d['type'] == 'note_on'

    def __repr__(self):
        return "{} {} ({})".format(self.channel, self.note, self.velocity)


class _MidiSong:

    def __init__(self, file, lights, scale):
        try:
            pygame.midi.init()
        except:
            pass
        self.file = file
        self.lights = lights
        self.scale = scale

    def _play(self, light, velocity, scale):
        light.on(min(255, velocity * 2 * scale))
        light.off(velocity * 6)

    def light_play(self, light, note, scale):
        if note.velocity <= 0:
            return
        thread = threading.Thread(
            target=self._play, args=(light, note.velocity, scale))
        thread.daemon = True
        thread.start()

    def play(self):
        mid = mido.MidiFile(self.file)
        player = pygame.midi.Output(0)
        global print_all
        try:
            last_time = time.time()
            for msg in mid.play():

                if msg.dict()['type'] == 'program_change':
                    player.set_instrument(
                        msg.dict()['program'], msg.dict()['channel'])
                    if print_instruments:
                        print(msg.dict()['channel'], msg.dict()['program'])

                if msg.dict()['type'] not in ['note_on', 'note_off']:
                    continue

                note = _MidiNote(msg)

                if note.on:
                    if print_all:
                        print(note)
                    player.note_on(note.note, note.velocity, note.channel)
                    if note.channel == 8:
                        print(',', round((time.time() - last_time) * 1000))
                        last_time = time.time()
                        print(str(note.note) + ',', note.velocity, end='')
                    if note.channel in self.lights:
                        self.light_play(self.lights[note.channel], note, self.scale)

                if not note.on:
                    if note.channel == 8:
                        print('OFF', note)
                    player.note_off(note.note, note.velocity, note.channel)

        except:
            del player
            raise
        del player

class MidiEffect:

    def __init__(self, file, instruments, scale):
        self.file = file
        self.scale = scale
        self.instruments = instruments

    def run(self, lights):
        for light in lights:
            light.off()
        mapping = {}
        for i in range(len(lights)):
            mapping[self.instruments[i]] = lights[i]
        song = _MidiSong(self.file, mapping, self.scale)
        song.play()