#AudioController produces audio using PyAudio, note whenever stream is paused, signal
#is modified such that "tick" (caused by discontinuity) is reduced

#fade in/out could be implemented over multiple callback blocks to lessen the impact of artifacts

import pyaudio
import numpy as np
from scipy import signal
import time

class AudioController:
    
    def __init__(self):

        self.audio = pyaudio.PyAudio()
        self.fs = 44100
        self.buffer = 1024
        self.channels = 1
        self.frameCount = 0
        self.volume = 50
        self.freqs = []
        self.waveform = "sine"
        self.enable = False

        self.stream = self.audio.open(format = pyaudio.paFloat32,
                                           channels = self.channels,
                                           rate = self.fs,
                                           frames_per_buffer = self.buffer,
                                           output = True,
                                           stream_callback = self.callback)

        #filter setup
        fc = 500
        w = fc / (self.fs / 2)
        self.b, self.a = signal.butter(10, w, "low")

    def generateSine(self, x):
        y = np.zeros(len(x))
        for freq in self.freqs:
            y += (self.volume / 300) * np.sin(2 * np.pi * freq * x)
        return y
    
    def generateSquare(self, x):
        y = np.zeros(len(x))
        for freq in self.freqs:
            y += (self.volume / 300) * np.sign(np.sin(2 * np.pi * freq * x))
        return y

    #PyAudio uses callback whenever new audio data is needed
    def callback(self, in_data, frame_count, time_info, status):
        
        #generate audio signal
        samples = np.arange(self.frameCount, self.frameCount + frame_count)
        x = samples / self.fs
        if (self.waveform == "sine"):
            y = self.generateSine(x)
        elif (self.waveform == "square"):
            y = self.generateSquare(x)

        #update frame count (part of callback function)
        self.frameCount += frame_count
        
        #continue or suspend stream
        if (self.enable):
            data = y.astype(np.float32).tobytes()
            return (data, pyaudio.paContinue)
        elif (self.waveform == "sine"):
            index = np.where(abs(y) < 0.01)[0][0]
            y = y[:index+1]
            y = np.concatenate((y, np.zeros(len(samples) - len(y))))
            y = signal.filtfilt(self.b, self.a, y)
            data = y.astype(np.float32).tobytes()
            return (data, pyaudio.paComplete)
        else:
            data = y.astype(np.float32).tobytes()
            return (data, pyaudio.paComplete)
        
    def startStream(self):
        self.enable = True
        self.stream.start_stream()

    def pauseStream(self):
        self.enable = False
        time.sleep(0.1)
        self.frameCount = 0
        if (self.stream):
            self.stream.stop_stream()

    
    def closeStream(self):
        if (self.stream):
            self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()