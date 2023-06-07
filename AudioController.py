#utilize callback mode, in callback mode a callback function is called by PyAudio
#whenver it needs more audio data to play, the callback function is responsible for
#generating or processing audio data on the fly and providing it to PyAudio
#https://www.youtube.com/watch?v=n2FKsPt83_A
#https://healthyalgorithms.com/2013/08/22/dsp-in-python-active-noise-reduction-with-pyaudio/

import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import wave
import time
import sys

class AudioController:
    
    def __init__(self):
        print("initialization start!")
        self.control = pyaudio.PyAudio()
        self.sampleRate = 44100
        self.duration = 5
        self.channels = 1
        self.frameCount = 0
        self.time = 0.0
        self.framesToPlay = int(self.sampleRate * self.duration)
        self.stream = self.control.open(format = pyaudio.paFloat32,
                                           channels = self.channels,
                                           rate = self.sampleRate,
                                           output = True,
                                           stream_callback = self.callback)
        self.stream.start_stream()
        print("initialization complete!")
        
    def callback(self, in_data, frame_count, time_info, status):
        
        #generate audio signal
        frequency = 1000
        samples = np.arange(self.frameCount, self.frameCount + frame_count)
        x = samples / self.sampleRate
        y =  0.1 * np.sin(2 * np.pi * frequency * x)
        data = y.astype(np.float32).tobytes()

        #suspend or continue the stream
        self.frameCount += frame_count
        if (self.frameCount >= self.framesToPlay):
            return (data, pyaudio.paComplete)
        else:
            return (data, pyaudio.paContinue)
    
    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.control.terminate()