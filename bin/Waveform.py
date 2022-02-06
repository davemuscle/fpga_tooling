#!/usr/bin/python

# DaveMuscle

"""
Python class for injecting stimulus waveforms into DUTs
I/O method is via raw text files as floats

Usage:
    x = Waveform()
    x.frequency = 440.0
    x.amplitude = 1.0
    x.samplerate = 44800
    x.length = 100
    x.generate_sine()
    x.file_export("test_input.txt")
    old_samples = x.samples
    < run FPGA design >
    x.file_import("test_output.txt")
    new_samples = x.samples
    < compare results > 
"""
import numpy as np

class Waveform:
    frequency = 440.0
    amplitude = 1.0
    offset = 0.0
    samplerate = 48000
    length = 1024
    samples = []

    def generate_dc(self):
        for n in range(self.length):
            self.samples.append(self.offset)

    def generate_sine(self):
        n = np.arange(self.length)
        samples = self.offset + self.amplitude*np.sin((2*np.pi*self.frequency*n)/self.samplerate)
        for s in samples:
            self.samples.append(s)

    def reset(self):
        self.samples = []

    # export implicit datatype as text
    def file_export(self, file):
        fd = open(file, "w")
        for sample in self.samples:
            fd.write(str(sample) + "\n")
        fd.close()

    # import text as float
    def file_import(self, file):
        self.reset()
        fd = open(file, "r")
        for line in fd.readlines():
            self.samples.append(float(line))
        fd.close()
