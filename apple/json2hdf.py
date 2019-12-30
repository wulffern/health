import pandas as pd
import json
import numpy as np
import sys


def main(file):
    ofile = file.replace(".json",".hdf")
    with open(file,"r",encoding="utf-8") as f:
        data = json.load(f)

    d_columns = {
        'creationDate':pd.datetime, 
        'device':'', 
        'endDate': pd.datetime, 
        'sourceName':'', 
        'sourceVersion':'',
       'startDate':pd.datetime, 
       'type':'', 
       'unit':'', 
       'value':np.float
    }

    l_columns = [
        'creationDate', 
        'device', 
        'endDate', 
        'sourceName',
        'sourceVersion',
       'startDate',
       'type',
       'unit',
       'value'
       ]
    
    #dtypes = [pd.datetime,'str',pd.datetime,'str','str',pd.datetime,'str','str','str',np.float]
    #df = pd.DataFrame(data,columns=l_columns,dtype=dtypes,index=[1])

    df = pd.DataFrame(data)
    df['creationDate'] = pd.to_datetime(df['creationDate'])
    df['startDate'] = pd.to_datetime(df['startDate'])
    df['endDate'] = pd.to_datetime(df['endDate'])
    df['device'] = str(df['device'])
    df['type'] = str(df['type'])
    df['unit'] = str(df['unit'])
    df['sourceName'] = str(df['sourceName'])
    df['sourceVersion'] = str(df['sourceVersion'])
    df['value'] = pd.to_numeric(df['value'])
    #df = df[df['startDate'] > "2019-12-01"]
    
    #print(df.dtypes)
    df.to_hdf(ofile,"apple")
    


if(len(sys.argv) > 0):
     main(sys.argv[1])
else:
    print("Error: json2hdf.py <jsonfile>")
