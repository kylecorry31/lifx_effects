import numpy as np
import pyaudio
import wave
import time
import threading
from scipy.fftpack import fft
from scipy.fftpack.basic import fft2

class _WavSong:
    def __init__(self, file, lights, scale, interval, bins, response_bins, alpha, equalize):
        self.p = pyaudio.PyAudio()
        self.file = file
        self.scale = scale
        self.lights = lights
        self.interval = interval
        self.stream = None
        self.last = time.time()
        self.last_fft_time = time.time()
        self.bins = bins
        self.response_bins = response_bins
        self.average = [0.0 for _ in response_bins]
        self.alpha = alpha
        self.equalize = equalize

    def __play_note(self, lights, reading):
        for i in range(len(lights)):
            if i < len(reading):
                lights[i].on(reading[i], self.interval)

    def __play_callback(self, in_data, frame_count, time_info, status):
        if self.file == 'microphone':
            data = np.frombuffer(in_data, dtype=np.int16)
        else:
            d = self.wf.readframes(frame_count)
            data = np.frombuffer(d, dtype=np.int16)
        dt = time.time() - self.last_fft_time
        self.last_fft_time = time.time()
        fft = np.abs(np.fft.fft(data)[:int(len(data)/2) + 1] * dt) / (327670 * np.math.log2(len(data)))
        binFFT = []
        inputChannelsPerBin = int(len(fft) / self.bins)
        for i in range(self.bins):
            binFFT.append(0.0)
            for channel in range(i * inputChannelsPerBin, (i+1) * inputChannelsPerBin):
                if (channel >= len(fft)):
                    break
                binFFT[i] += fft[i]
            binFFT[i] /= inputChannelsPerBin
        binFFT = np.array(binFFT)
        if self.equalize:
            maximum = np.linalg.norm(binFFT)
            if maximum > 0:
                binFFT = binFFT / maximum
        reading = binFFT[self.response_bins] * 255 * self.scale
        for i in range(len(self.average)):
            self.average[i] = self.average[i] * self.alpha + reading[i] * (1 - self.alpha)
        print("Max bin:", np.argmax(binFFT), "Bins:", np.round(self.average))
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

class AudioSpectrumEffect:

    def __init__(self, wav_file, scale, resolution = 0.05, bins = None, num_bins = None, loop = False, equalize = True, alpha = 0.8):
        self.file = wav_file
        self.scale = scale
        self.resolution = resolution
        self.num_bins = num_bins
        self.bins = bins
        self.alpha = alpha
        self.equalize = equalize
        self.loop = loop

    def run(self, lights):
        first = True
        while first or self.loop:
            first = False
            for light in lights:
                light.off()
            num_bins = len(lights) if self.num_bins is None else self.num_bins
            bins = [i for i in range(len(lights))] if self.bins is None else self.bins
            song = _WavSong(self.file, lights, self.scale, self.resolution, num_bins, bins, self.alpha, self.equalize)
            song.play()
