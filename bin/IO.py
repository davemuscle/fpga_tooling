#!/usr/bin/python

# DaveMuscle

# export implicit datatype as text
def fexport(file, samples):
    fd = open(file, "w")
    for sample in samples:
        fd.write(str(sample) + "\n")
    fd.close()

# import text as cast type
def fimport(file, cast=float):
    samples = []
    fd = open(file, "r")
    for line in fd.readlines():
        samples.append(float(line))
    fd.close()
    return samples
