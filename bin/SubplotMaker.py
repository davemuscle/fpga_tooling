#!/usr/bin/python

# DaveMuscle

from matplotlib.pyplot import *
from pydoc import locate

class SubplotMaker:
    rows = 0
    cols = 0
    figtitle = ""
    data = []
    xdata = []
    ydata = []
    xlabels = []
    ylabels = []
    stitles = []

    def __init__(self, file):
        fd = open(file, "r")
        self.data = fd.readlines()
        fd.close()

    def get_rows_cols(self):
        line = self.data[0]
        line = line.split(',')
        for item in line:
            if "rows" in item:
                self.rows = int(item.split('=')[1].strip())
            if "cols" in item:
                self.cols = int(item.split('=')[1].strip())
            if "title" in item:
                self.figtitle = item.split('=')[1].strip()

    def get_plot_params(self):
        num_plots = self.rows * self.cols
        self.xlabels = [""]*num_plots
        self.ylabels = [""]*num_plots
        self.stitles = [""]*num_plots
        for i in range(num_plots):
            line = self.data[i+1].strip()
            if(line):
                items = line.split(',')
                for item in items:
                    if "xlabel" in item:
                        self.xlabels[i] = item.split('=')[1].strip()
                    if "ylabel" in item:
                        self.ylabels[i] = item.split('=')[1].strip()
                    if "title" in item:
                        self.stitles[i] = item.split('=')[1].strip()

    def get_raw(self):
        self.xdata = [[] for _ in range(self.rows*self.cols)]
        self.ydata = [[] for _ in range(self.rows*self.cols)]

        idx = 1 + self.rows * self.cols
        for i in range(idx, len(self.data)):
            plot_num = 0
            line = self.data[i].strip()
            for plot_data in line.split("::"):
                num = plot_data.split(',')
                self.xdata[plot_num].append(num[0])
                self.ydata[plot_num].append(num[1])
                plot_num = plot_num + 1

    def debug(self):
        print("rows=" + str(self.rows))
        print("cols=" + str(self.cols))
        print("figtitle=" + self.figtitle)
        print("xlabels:")
        print(self.xlabels)
        print("ylabels:")
        print(self.ylabels)
        print("xdata:")
        print(self.xdata)
        print("ydata:")
        print(self.ydata)


    def run(self):
        for i in range(self.rows*self.cols):
            subplot(self.rows * 100 + self.cols * 10 + (i+1))
            plot(self.xdata[i], self.ydata[i])
            title(self.stitles[i])
            xlabel(self.xlabels[i])
            ylabel(self.ylabels[i])
        suptitle(self.figtitle)
        #tight_layout()
        show()

if __name__ == '__main__':
    x = SubplotMaker(sys.argv[1])
    x.get_rows_cols()
    x.get_plot_params()
    x.get_raw()
    #x.debug()
    x.run()





