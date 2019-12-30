#!/Users/wulff/anaconda3/bin/python3.6
######################################################################
##        Copyright (c) 2018 Carsten Wulff Software, Norway 
## ###################################################################
## Created       : wulff at 2018-8-3
## ###################################################################
##  The MIT License (MIT)
## 
##  Permission is hereby granted, free of charge, to any person obtaining a copy
##  of this software and associated documentation files (the "Software"), to deal
##  in the Software without restriction, including without limitation the rights
##  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
##  copies of the Software, and to permit persons to whom the Software is
##  furnished to do so, subject to the following conditions:
## 
##  The above copyright notice and this permission notice shall be included in all
##  copies or substantial portions of the Software.
## 
##  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##  SOFTWARE.
##  
######################################################################
import pandas as pd
import matplotlib.dates as mdates
from scipy.signal import savgol_filter
import math
import numpy as np
import sys
import io
import re
import os
import json
import datetime

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

threshold = 150

def main(filename):
    havg = 'heart-avg'
    hmax = 'heart-max'
    hmin = 'heart-min'
    weight = 'weight'

    with open(filename) as f:
        data = json.load(f)

        dhdate = list()
        dhavg = list()
        dhmax = list()
        dhmin  = list()
        dweight = list()
        dwdate = list()
        dthres = list()
        i = 0
        dthres.append(110)
        for key in sorted(data):
            if(data[key][hmax] != -1):
                dhdate.append(key)
                dhavg.append(data[key][havg])
                dhmin.append(data[key][hmin])
                dhmax.append(data[key][hmax])
                if(i > 0):
                    if(data[key][hmax] > threshold):

                        dthres.append(dthres[i-1] - 0.3)
                    else:
                        dthres.append(dthres[i-1] + 0.1)

                i = i  + 1

            if(data[key][weight] != -1):
                dwdate.append(key)
                dweight.append(data[key][weight])

        pp = PdfPages(filename + ".pdf")

 #       dhmax_curvefit = savgol_filter(dhmax, 51, 3)
        
        plt.plot(pd.to_datetime(dhdate),dthres)
#        plt.plot(pd.to_datetime(dhdate),dhmax_curvefit,linestyle='None',marker='.',color='r')
#        plt.plot(pd.to_datetime(dhdate),dhmin)
        plt.plot(pd.to_datetime(dwdate),dweight)
#            yhat = savgol_filter(vals, 51, 3)

        plt.xlabel('Date [n]')
        plt.ylabel("Kostnad [kr]")
#        plt.grid(True)
        plt.xticks(rotation=90)
        plt.xlim([datetime.date(2016, 1, 1), datetime.datetime.now()])
        plt.savefig(pp,format='pdf')
        plt.close('all')
        plt.autoscale()        
        pp.close()

        


if(len(sys.argv) > 0):
     main(sys.argv[1])
else:
    print("Error: plot.py <directory>");
