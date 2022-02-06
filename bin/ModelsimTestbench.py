#!/usr/bin/python

# DaveMuscle

"""
Python class for running a simulation for via Modelsim
Design parameters and files are parsed from a textfile that takes the form:

    #DEF CLKRATE = 5000
    #DEF USE_THIS_FEATURE = TRUE
    #ENT my_design_tb
    #SRC my_design_tb.sv
    #SRC my_design.sv
    #SRC my_design_fifo.sv

Usage:
    x = ModelsimTestbench()
    x.parse("my_design_list.txt")
    x.compile()
    x.run()
"""

import os # for system call
   
class ModelsimTestbench:

    entity = ""
    sources = []
    defines = {}

    # open text file, read directives, and add to class members
    def parse(self, listfile):
        fd = open(listfile, "r")
        for line in fd.readlines():
            line = line.strip()
            # first four characters contain directive, like #DEF
            directive = line[0:4]
            # rest of the string contains target
            target = line[4:len(line)].strip()
            # add top-level entity
            if(directive == "#ENT"):
                self.entity = target
            # add source files
            if(directive == "#SRC"):
                self.sources.append(target)
            # add parameter defines
            if(directive == "#DEF"):
                # define directives seprated by = 
                target = target.replace(' ', '').split('=')
                self.defines[target[0]] = target[1]
        fd.close()

    def print_parsed(self):
        # print out class members from debug
        print("Modelsim source file output parse:")
        print("*  Entity: " + self.entity)
        for define in self.defines:
            print("*    Define: " + define + " = " + self.defines[define])
        for source in self.sources:
            print("*    Source: " + source)

    # run vlog
    def compile(self):
        cmd = "vlog"
        for source in self.sources:
            cmd = cmd + " " + source
        print(cmd)
        os.system(cmd)

    # run vsim
    def run(self):
        cmd = "vsim -c -do \"run -all\"" 
        cmd = cmd + " " + self.entity
        for define in self.defines:
            cmd = cmd + " -G" + define + "=" + self.defines[define]
        print(cmd)
        os.system(cmd)

    def clean(self):
        cmd = "rm -rf work/* transcript *.vcd *.vcd.fst"
        os.system(cmd)
