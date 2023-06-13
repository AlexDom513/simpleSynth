#utilize callback mode, in callback mode a callback function is called by PyAudio
#whenver it needs more audio data to play, the callback function is responsible for
#generating or processing audio data on the fly and providing it to PyAudio
#https://www.youtube.com/watch?v=n2FKsPt83_A
#https://healthyalgorithms.com/2013/08/22/dsp-in-python-active-noise-reduction-with-pyaudio/

import pyaudio
import numpy as np
import time

class AudioController:
    
    def __init__(self):
        print("initialization start!")
        self.control = pyaudio.PyAudio()
        self.sampleRate = 44100
        self.duration = 5
        self.enable = False
        self.channels = 1
        self.frameCount = 0
        self.count = 0
        print("initialization complete!")
        
    def callback(self, in_data, frame_count, time_info, status):
        
        #generate audio signal
        samples = np.arange(self.frameCount, self.frameCount + frame_count)
        print(str(self.frameCount) + " : " + str(self.frameCount + frame_count))
        x = samples / self.sampleRate

        y =  1 * np.sin(2 * np.pi * self.freq * x)
        rate = 500
        if (self.frameCount < 576 and self.enable):
            print('trigger1')
            z = 1 - np.exp(-rate*x)
            y = y * z

        data = y.astype(np.float32).tobytes()
        self.frameCount += frame_count
        
        #suspend or continue the stream
        if (self.enable):
            #np.savetxt('varA' + str(self.count) + '.txt', y, fmt='%lf')
            self.count += 1
            return (data, pyaudio.paContinue)
        else:
            k = np.exp(-(x / 4096)**5)
            y = y * k
            np.savetxt('varB.txt', y, fmt='%lf')
            return (data, pyaudio.paComplete)
        
    def startStream(self, freq):
        self.enable = True
        self.freq = freq
        self.stream = self.control.open(format = pyaudio.paFloat32,
                                           channels = self.channels,
                                           rate = self.sampleRate,
                                           frames_per_buffer = 4096,
                                           output = True,
                                           stream_callback = self.callback)
        self.stream.start_stream()

        #idea, use different threads to generate and play sound
        #1st thread is generator, as long as a note is pressed generate the sound
        #2nd thread is player, all generated sounds get dumped to the player

    def pauseStream(self):
        self.enable = False
        time.sleep(.1)
        self.frameCount = 0
        if (self.stream):
            self.stream.stop_stream()
    
    def closeStream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.control.terminate()