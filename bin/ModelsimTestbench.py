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
import argparse # for command-line usage

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
        if(os.system(cmd) != 0):
            raise Exception('Modelsim compilation failed!')

    # run vsim
    def run(self):
        cmd = "vsim -c -do \"run -all\"" 
        cmd = cmd + " " + self.entity
        for define in self.defines:
            cmd = cmd + " -G" + define + "=" + self.defines[define]
        print(cmd)
        if(os.system(cmd) != 0):
            raise Exception('Modelsim elaboration failed!')

    # clean up directory
    def clean(self):
        cmd = "rm -rf work transcript *.vcd *.vcd.fst"
        if(os.system(cmd) != 0):
            raise Exception('Modelsim clean failed!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Helper class for Modelsim simulation')
    parser.add_argument('--cmd', metavar='file.txt', required=True, nargs=1, type=str, help = 'simulation directive text file')
    parser.add_argument('--clean', action='store_const', const=1, help='clean directory')
    parser.add_argument('--print_parse', action='store_const', const=1, help='print post-parsed data')
    parser.add_argument('--compile', action='store_const', const=1, help='compile simulation')
    parser.add_argument('--run', action='store_const', const=1, help='elaborate simulation, compilation must have been run')
    parser.add_argument('--all', action='store_const', const=1, help='run all of the above')

    args = parser.parse_args()
    tb = ModelsimTestbench()
    if(args.clean or args.all):
        tb.clean()
    tb.parse(args.cmd[0])
    if(args.print_parse or args.all):
        tb.print_parsed()
    if(args.compile or args.all):
        tb.compile()
    if(args.run or args.all):
        tb.run()
