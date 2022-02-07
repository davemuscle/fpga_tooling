#!/usr/bin/python

# DaveMuscle

"""
Python class for injecting stimulus waveforms into DUTs

Usage:
"""
import numpy as np

class Waveform:
    frequency = 440.0
    amplitude = 1.0
    offset = 0.0
    samplerate = 48000
    length = 1024
    samples = []

    def set_waveform(self, frequency = 440.0, amplitude = 1.0, offset = 0.0, samplerate = 48000):
        self.frequency = frequency
        self.amplitude = amplitude
        self.offset = offset
        self.samplerate = samplerate

    def set_length(self, length = 1024):
        self.length = length

    def generate_dc(self):
        for n in range(self.length):
            self.samples.append(self.offset)

    def generate_sine(self):
        n = np.arange(self.length)
        samples = self.offset + self.amplitude*np.sin((2*np.pi*self.frequency*n)/self.samplerate)
        for s in samples:
            self.samples.append(s)

    def clear_samples(self):
        self.samples = []

    def get_samples(self):
        return self.samples
