#!/usr/bin/python

# Dave Muscle
# from the command line, eg: make sim sim_list=xyz

"""
  Helper for running Digilent's Analog Discovery via Python
  Adapted mostly from their sample code
"""

import sys
from time import sleep
sys.path.append("/usr/share/digilent/waveforms/samples/py")

from ctypes import *
from dwfconstants import *

class DigilentAnalogDiscovery:

    loud = 1

    def __init__(self):
        # Load Linux Library
        self.dwf = cdll.LoadLibrary("libdwf.so")

    def enable_prints(self):
        self.loud = 1
    def disable_prints(self):
        self.loud = 0

    def get_version(self):
        if(self.loud):
            version = create_string_buffer(16)
            self.dwf.FDwfGetVersion(version)
            print("DWF Version: " + str(version.value))

    # open device, defaults to first (-1)
    def open_device(self, device=-1):
        self.hdwf = c_int()
        self.dwf.FDwfDeviceOpen(c_int(device), byref(self.hdwf))
        if(self.loud):
            if self.hdwf.value == hdwfNone.value:
                print("Failed to open device")
            else:
                print("Opened device")

    def close_device(self):
        self.dwf.FDwfDeviceClose(self.hdwf)
        if(self.loud):
            print("Closed device")

    def wavegen_config_sine_out(self, channel=0, freq=100, amp=1.0, offset=0):
        self.dwf.FDwfDeviceAutoConfigureSet   (self.hdwf, channel)
        self.dwf.FDwfAnalogOutNodeEnableSet   (self.hdwf, channel, AnalogOutNodeCarrier, c_bool(True))
        self.dwf.FDwfAnalogOutNodeFunctionSet (self.hdwf, channel, AnalogOutNodeCarrier, funcSine)
        self.dwf.FDwfAnalogOutNodeFrequencySet(self.hdwf, channel, AnalogOutNodeCarrier, c_double(freq))
        self.dwf.FDwfAnalogOutNodeAmplitudeSet(self.hdwf, channel, AnalogOutNodeCarrier, c_double(amp))
        self.dwf.FDwfAnalogOutNodeOffsetSet   (self.hdwf, channel, AnalogOutNodeCarrier, c_double(offset))
        self.dwf.FDwfAnalogOutConfigure       (self.hdwf, channel, c_bool(True))

    def setup_custom_data(self, size):
        self.custom_data = (c_double*size)()
        self.custom_len = c_int(size)

    def wavegen_config_custom_out(self, channel=0, freq=100, amp=1.0, offset=0):
        self.dwf.FDwfDeviceAutoConfigureSet   (self.hdwf, channel)
        self.dwf.FDwfAnalogOutNodeEnableSet   (self.hdwf, channel, AnalogOutNodeCarrier, c_bool(True))
        self.dwf.FDwfAnalogOutNodeFunctionSet (self.hdwf, channel, AnalogOutNodeCarrier, funcCustom)
        self.dwf.FDwfAnalogOutNodeDataSet     (self.hdwf, channel, AnalogOutNodeCarrier, self.custom_data, self.custom_len)
        self.dwf.FDwfAnalogOutNodeFrequencySet(self.hdwf, channel, AnalogOutNodeCarrier, c_double(freq))
        self.dwf.FDwfAnalogOutNodeAmplitudeSet(self.hdwf, channel, AnalogOutNodeCarrier, c_double(amp))
        self.dwf.FDwfAnalogOutNodeOffsetSet   (self.hdwf, channel, AnalogOutNodeCarrier, c_double(offset))
        self.dwf.FDwfAnalogOutConfigure       (self.hdwf, channel, c_bool(True))

    def scope_config_read_buffer(self, buffer=4096, channel=0, samplerate=20000000.0, range=5.0):
        sts = c_byte()
        samples = (c_double*buffer)()
        self.dwf.FDwfAnalogInFrequencySet(self.hdwf, c_double(samplerate))
        self.dwf.FDwfAnalogInBufferSizeSet(self.hdwf, c_int(buffer)) 
        self.dwf.FDwfAnalogInChannelEnableSet(self.hdwf, c_int(-1), c_bool(True))
        self.dwf.FDwfAnalogInChannelRangeSet(self.hdwf, c_int(-1), c_double(range))
        self.dwf.FDwfAnalogInChannelFilterSet(self.hdwf, c_int(-1), filterDecimate)
        
        sleep(2)
        self.dwf.FDwfAnalogInConfigure(self.hdwf, c_int(1), c_int(1))
        
        while True:
            self.dwf.FDwfAnalogInStatus(self.hdwf, c_int(1), byref(sts))
            if sts.value == DwfStateDone.value :
                break
            sleep(0.1)
        
        if(channel == 0):
            self.dwf.FDwfAnalogInStatusData(self.hdwf, 0, samples, buffer) # get channel 1 data
            self.dwf.FDwfDeviceCloseAll()
        elif(channel == 1):
            self.dwf.FDwfAnalogInStatusData(self.hdwf, 1, samples, buffer) # get channel 2 data
            self.dwf.FDwfDeviceCloseAll()
        return samples
