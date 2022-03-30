#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame import *
import pygame
import time
import numpy
import pygame.sndarray

sample_rate = 44100


def play_for(sample_array, ms, volLeft, volRight):
    sound = pygame.sndarray.make_sound(sample_array)
    beg = time.time()
    channel = sound.play(-1)
    channel.set_volume(volLeft, volRight)
    pygame.time.delay(ms)
    sound.stop()
    end = time.time()
    return beg, end


def sine_array_onecycle(hz, peak):
    length = sample_rate / float(hz)
    omega = numpy.pi * 2 / length
    xvalues = numpy.arange(int(length)) * omega
    return peak * numpy.sin(xvalues)


def sine_array(hz, peak, n_samples=sample_rate):
    return numpy.int16(numpy.resize(sine_array_onecycle(hz, peak), (n_samples,)))


def main():
    pygame.mixer.pre_init(sample_rate, -16, 1)  # 44.1kHz, 16-bit signed, stereo
    pygame.init()
    f = sine_array(1000, 1)
    # f = numpy.array(zip(f, f))
    # f = numpy.array(f)

    play_for(f, 2000, 1., 0.)


if __name__ == '__main__':
    main()
#
