import numpy as np
import pyaudio
import wave
import time
import threading

class _WavSong:
    def __init__(self, file, lights, scale, interval, alpha):
        self.p = pyaudio.PyAudio()
        self.file = file
        self.scale = scale
        self.lights = lights
        self.interval = interval
        self.alpha = alpha
        self.average = 0.0
        self.stream = None
        self.last = time.time()

    def __play_note(self, lights, reading):
        for light in lights:
            light.on(reading, self.interval)

    def __play_callback(self, in_data, frame_count, time_info, status):
        if self.file == 'microphone':
            data = np.frombuffer(in_data, dtype=np.int16)
        else:
            d = self.wf.readframes(frame_count)
            data = np.frombuffer(d, dtype=np.int16)
        reading = (np.max(np.abs(data)) / 32767.0) * 255 * self.scale
        self.average = self.average * self.alpha + reading * (1 - self.alpha)
        if time.time() - self.last > self.interval:
            self.last = time.time()
            thread = threading.Thread(target=self.__play_note, args=(self.lights, self.average))
            thread.daemon = True
            thread.start()
        return (data, pyaudio.paContinue)

    def play(self):
        if self.file == 'microphone':
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 2
            RATE = 44100
            self.stream = self.p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                input=True, frames_per_buffer=CHUNK, stream_callback=lambda in_data, frame_count, time_info, status: self.__play_callback(in_data, frame_count, time_info, status))
        else:
            self.wf = wave.open(self.file, 'rb')
            self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                channels=self.wf.getnchannels(), rate=self.wf.getframerate(),
                            output=True, stream_callback=lambda in_data, frame_count, time_info, status: self.__play_callback(in_data, frame_count, time_info, status))
        self.stream.start_stream()
        while self.stream.is_active():
            time.sleep(0.1)
        self.stop()

    def stop(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

class AudioAmplitudeEffect:

    def __init__(self, file, scale, resolution=0.05, alpha=0.8, loop=False):
        self.file = file
        self.scale = scale
        self.resolution = resolution
        self.alpha = alpha
        self.loop = loop

    def run(self, lights):
        first = True
        while first or self.loop:
            first = False
            for light in lights:
                light.off()
            song = _WavSong(self.file, lights, self.scale, self.resolution, self.alpha)
            song.play()
