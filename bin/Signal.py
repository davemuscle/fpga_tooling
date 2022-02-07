#!/usr/bin/python

# DaveMuscle

"""

"""

import numpy as np
from Waveform import *

# Inherit Waveform class
class Signal(Waveform):
    dft_size  = 1024 
    def config_dft(self, size = 1024):
        self.dft_size = size

    # generate range of log-spaced frequencies
    def set_sweep(self, start = 440.0, end = 3520.0, steps = 36, cycles_per = 1):
        self.sweep_mult = (float(end) / float(start)) ** float(1.0/float(steps-1))
        self.sweep_frequency = []
        self.sweep_length = []
        freq = start
        for i in range(steps):
            self.sweep_frequency.append(freq)
            self.sweep_length.append(int((self.samplerate / self.sweep_frequency[i]) * cycles_per))
            freq *= self.sweep_mult

    # generate sample data
    def generate_sine_sweep(self):
        for i in range(len(self.sweep_frequency)):
            self.frequency = self.sweep_frequency[i]
            self.length = self.sweep_length[i]
            self.generate_sine()

    # Convert array of samples to single amplitude = peak-peak / 2
    def get_amplitude(self, samples):
        low = samples[0]
        high = samples[0]
        for x in range(1, len(samples)):
            if(samples[x] < low):
                low = samples[x];
            if(samples[x] > high):
                high = samples[x];
        return ((high-low)/2)

    # get DC value
    def get_dc(self, samples):
        return (sum(samples)/len(samples))

    # get RMS of the set
    def get_rms(self, samples):
        sq_sum = 0
        for x in samples:
            sq_sum += (x**2)
        sq_sum /= len(samples)
        return np.sqrt(sq_sum)

    # Calculate DFT, skips DC bin and only gives up to Fs/2
    # Also provides log output based on Waveform.amplitude
    def get_dft(self, samples):
        XQ = [0]*self.dft_size
        XI = [0]*self.dft_size

        for k in range(self.dft_size):
            for n in range(len(samples)):
                XQ[k] = XQ[k] + samples[n] * (np.cos(2*3.14*k*n/self.dft_size))
                XI[k] = XI[k] + samples[n] * -1 * (np.sin(2*3.14*k*n/self.dft_size))

        XM   = [0]*((self.dft_size>>1)-1)
        Xf   = [0]*((self.dft_size>>1)-1)
        XM_l = [0]*len(XM)

        for k in range((self.dft_size>>1)-1):
            Xf[k] = k * self.samplerate / self.dft_size
            XM[k] = np.sqrt(XQ[k+1]**2 + XI[k+1]**2) / (self.dft_size/2)
            XM_l[k] = 20*np.log10(XM[k] / self.amplitude)

        return Xf, XM, XM_l

    # Set the waveform frequency to match the closest DFT bin 
    def set_frequency_to_dft_bin(self):
        delta = self.samplerate / self.dft_size
        fbin = round(self.frequency / delta)  
        self.frequency = fbin * delta

    # Get signal-to-noise ratio via DFT magnitudes
    def get_snr(self, mags):
        idx =  mags.index(max(mags))
        top = mags[idx]
        mags[idx] = 0
        low = self.get_rms(mags)
        mags[idx] = top
        return 20*np.log10(top/low)

