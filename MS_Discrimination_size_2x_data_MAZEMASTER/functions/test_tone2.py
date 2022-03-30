import numpy as np
import pygame as pg
import time
import matplotlib.pyplot as plt


frequency, samplerate, duration = 400, 44100, 20000
nchannels = 1 # change to 2 for stereo 
pg.mixer.pre_init(channels=nchannels, frequency=samplerate)
pg.init()

sinusoid = (2**15 - 1) * np.sin(2.0 * np.pi * frequency * np.arange(0, duration) / float(samplerate))
samples = np.array(sinusoid, dtype=np.int16)
if nchannels > 1: #copy mono signal to two channels
    samples = np.tile(samples, (nchannels, 1)).T
sound = pg.sndarray.make_sound(samples)
sound.play()

time.sleep(duration/float(samplerate))
plt.plot(samples)
plt.show()
