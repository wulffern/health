import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import datetime
import seaborn as sns
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter




def adorne(ax):
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(DateFormatter("%Y"))
    ax.grid(color='lightgray')
    ax.autoscale()

def add_annotation(date,text,xytext):
    x0 = pd.Timestamp(date)
    y0 = hr.asof(x0)
    ax0.annotate(text,(x0,y0),xytext=xytext, textcoords='axes fraction',
            arrowprops=dict(width=1,facecolor='red', shrink=1),
            horizontalalignment='right', verticalalignment='top',)


max = 193
mult_medium = 2
mult_hard = 8

def aggregateDay(df):

    rest = df.between(left=0,right=max*0.6).sum()
    light = df.between(left=max*0.6,right=max*0.75).sum()
    medium = df.between(left=max*0.75,right=max*0.85).sum()
    hard = df.between(left=max*0.85,right=max*1.5).sum()
    date = df.index[0]
    score = light + medium*mult_medium + hard*mult_hard

    if(score > 60):
        score = 60

    score = score/60.0
    #print(f"{date}: rest = {rest}, light = {light}, medium = {medium}, hard = {hard}, score={score}")
    return score


    
#- Read and filter data
df = pd.read_hdf("tmp/HKQuantityTypeIdentifierHeartRate.hdf")
df = df[df["startDate"] > "2016-08-14"]
df.set_index('startDate',inplace=True)
df.drop_duplicates(subset="endDate",inplace=True)
df = df[['value']]

df = df.resample('T').ffill()

hr = df['value']

r = hr.resample('D')
hr = r.apply(aggregateDay)

hr = hr.rolling(7).sum()

hr.to_hdf("tmp/training_days.hdf","apple")


#- Plot stuff
sns.set()
fig, (ax0) = plt.subplots(nrows=1, ncols=1, constrained_layout=True) 
fig.set_figheight(8)
fig.set_figwidth(10)
ax0.plot(hr.index,hr)
ax0.set_title("Training days per week ")
ax0.set_ylabel("Days")

adorne(ax0)

#- Annotate text
#add_annotation("2017-01-26","No candy, chips or chocolate",(0.4,0.99))
#add_annotation("2018-05-15","When do I rest, instead of when do I exercise?",(0.9,0.7))
#add_annotation("2019-07-05","No bread",(0.6,0.2))
#add_annotation("2019-10-01","No pasta etc",(0.85,0.5))
#add_annotation("2019-11-14","No meat",(0.95,0.4))

plt.show()
#plt.savefig("weight.png")





