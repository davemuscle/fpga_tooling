#!/usr/bin/python

# DaveMuscle

"""

"""

import numpy as np

# create sine wave
def generate_sine(frequency=440.0, amplitude=1.0, offset=0, samplerate=48000, length=256):
    n = np.arange(length)
    samples = offset + amplitude*np.sin((2*np.pi*frequency*n)/samplerate)
    return samples

# generate range of log-spaced frequencies
def get_sweep(start = 440.0, end = 3520.0, steps = 36):
    sweep_mult = (float(end) / float(start)) ** float(1.0/float(steps-1))
    sweep_frequency = []
    freq = start
    for i in range(steps):
        sweep_frequency.append(freq)
        freq *= sweep_mult
    return sweep_frequency

# Convert array of samples to single amplitude = peak-peak / 2
def get_amplitude(samples):
    low = samples[0]
    high = samples[0]
    for x in range(1, len(samples)):
        if(samples[x] < low):
            low = samples[x];
        if(samples[x] > high):
            high = samples[x];
    return ((high-low)/2)

# get DC value
def get_dc(samples):
    return (sum(samples)/len(samples))

# get RMS of the set
def get_rms(samples):
    sq_sum = 0
    for x in samples:
        sq_sum += (x**2)
    sq_sum /= len(samples)
    return np.sqrt(sq_sum)

# Calculate DFT
def get_dft(samples=[], samplerate=48000, dft_size=256):
    XQ = [0]*dft_size
    XI = [0]*dft_size

    for k in range(dft_size):
        for n in range(len(samples)):
            XQ[k] = XQ[k] + samples[n] * (np.cos(2*3.14*k*n/dft_size))
            XI[k] = XI[k] + samples[n] * -1 * (np.sin(2*3.14*k*n/dft_size))
    return XQ, XI

# Calculate DFT mags and freq bins, skips DC and > Fs/2
def get_dft_mags(dft_calc=(), samplerate=48000, dft_size=256): 
    XQ = dft_calc[0]
    XI = dft_calc[1]
    XM   = [0]*((dft_size>>1)-1)
    Xf   = [0]*((dft_size>>1)-1)

    for k in range((dft_size>>1)-1):
        Xf[k] = k * samplerate / dft_size
        XM[k] = np.sqrt(XQ[k+1]**2 + XI[k+1]**2) / (dft_size/2)

    return Xf, XM

# Set the waveform frequency to match the closest DFT bin 
def set_frequency_to_dft_bin(frequency=440.0, samplerate=48000, dft_size=256):
    delta = samplerate / dft_size
    fbin = round(frequency / delta)  
    return fbin*delta

# Get signal-to-noise ratio via DFT magnitudes
# Might be a good idea to cut out the DC bin before calling
def get_snr(mags=[], forgiveness=4):
    mags_copy = [i for i in mags]
    idx =  mags.index(max(mags))
    top = mags[idx]
    mags_copy[idx] = 0
    for i in range(1,int((forgiveness/2)+1)):
        mags_copy[idx+i] = 0
        mags_copy[idx-i] = 0
    low = get_rms(mags_copy)
    return 20*np.log10(top/low)

# Get THD+N
def get_thdn(mags=[], targetfreq = 440.0, dft_size = 1024, samplerate=44800):
    mags_copy = [i for i in mags]
    idx = mags_copy.index(max(mags_copy))
    fundamental = mags_copy[idx]
    mags_copy[idx] = 0
    sum_harmonics = 0
    harmonic = 2
    curr_freq = targetfreq * harmonic
    delta = float(samplerate) / float(dft_size)
    while(curr_freq < samplerate/2):
        curr_idx = int(round(float(curr_freq) / float(delta)))
        sum_harmonics = sum_harmonics + mags_copy[curr_idx]
        mags_copy[curr_idx] = 0
        harmonic = harmonic + 1
        curr_freq = targetfreq * harmonic
    noise = get_rms(mags_copy)
    return (sum_harmonics + noise)/fundamental

def apply_hann_window(samples, alpha):
    i = 0
    w = []
    for sample in samples:
        v = np.cos(2*np.pi*float(i)/float(len(samples)))
        v = 1 -v
        i = i + 1
        v = v * alpha
        w.append(v * sample)
    return w

def apply_tukey_window(samples, alpha):
    w = [0]*len(samples)
    lower_lim = int(alpha*len(samples)/2)
    for n in range(lower_lim):
        w[n] = 0.5*(1 - np.cos(2.0*np.pi*n/(alpha*len(samples))))
    for n in range(lower_lim,int(len(samples)/2)):
        w[n] = 1
    for n in range(int(len(samples)/2), len(samples)):
        w[n] = w[len(samples)-n-1]
    for n in range(len(samples)):
        w[n] = w[n] * samples[n]
    return w

def remove_dc(samples):
    dc = get_dc(samples)
    return [x-dc for x in samples]
