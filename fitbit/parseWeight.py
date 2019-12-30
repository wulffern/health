import pandas as pd
import sys
import os
import re
import json

data = list()

def readFiles(dir):
    for root, subdirs, files in os.walk(dir):
        for file in files:
            if(re.search('weight.*\.json',file)):
                parseFile(root + "/" + file)
        for leafdir in subdirs:
            readFiles(root + "/" + dir)

def parseFile(file):
    with open(file) as f:
        jobj = json.load(f)
        for item in jobj:
            data.append(item)

def main(path):
    readFiles(path)
    with open("tmp/fitbit_weight.json","w") as f:
        json.dump(data,f,indent=4)
    df = pd.read_json("tmp/fitbit_weight.json")
    df.to_hdf("tmp/fitbit_weight.hdf","weight")

if(len(sys.argv) > 0):
     main(sys.argv[1])
else:
    print("Error: parseEight.py <fitbit directory>");


