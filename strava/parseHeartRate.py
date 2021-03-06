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

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

data = dict()

def readFiles(dir):
    for root, subdirs, files in os.walk(dir):
        for file in files:
            if(re.search('\.csv',file)):
                parseFile(root + "/" + file)
        for leafdir in subdirs:
            readFiles(root + "/" + dir)

def readEng(str):
    unit = ""    
    m = re.search(r'([-+\d\.]+)([a-zA-Z%]+)',str);
    if(m != None and len(m.groups()) == 2):
        num = float(m.group(1))
        unit = m.group(2)
    else:
        num = float(str)
    return (num,unit)

def parseFile(file):

    havg = 'heart-avg'
    hmax = 'heart-max'
    hmin = 'heart-min'
    weight = 'weight'

    df = pd.read_csv(file,skiprows=1)
    for index,row in df.iterrows():
        date = pd.to_datetime(row[0])
        key = date.year + "-" + date.month + "-" + date.day
        if(key not in data):
            data[key] = {}
            data[key][havg] = -1
            data[key][hmin] = 300
            data[key][hmax] = -1
            data[key][weight] = -1
        else
            if('heart-rate-bpm' in row):
                h = row['heart-rate-bpm']
                if(data[key][havg] == -1):
                    data[key][havg] = h
                else:
                    data[key][havg] = (h + data[key][havg])/2

                if(h > data[key][hmax]):
                    data[key][hmax] = h

                if(h < data[key][hmin]):
                    data[key][hmin] = h
                    
            else if('weight-kilograms' in row):
                data[key][weight] = data[key]['weight-kilograms']
                

def main(rootdir):
    readFiles(rootdir)
    pp = PdfPages(rootdir + ".pdf")
    json = json.dumps(dict)
    f = open("dict.json","w")
    f.write(json)
    f.close()

    
if(len(sys.argv) > 0):
     main(sys.argv[1])
else:
    print("Error: atelog.py <directory>");
