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
    y0 = weight.asof(x0)
    ax0.annotate(text,(x0,y0),xytext=xytext, textcoords='axes fraction',
            arrowprops=dict(width=1,facecolor='red', shrink=1),
            horizontalalignment='right', verticalalignment='top',)

    
#- Read and filter data
df = pd.read_hdf("tmp/fitbit_weight.hdf")
df = df[df["date"] > "2016-08-13"]
df["date"] = pd.to_datetime(df["date"])
df["time"] = pd.to_timedelta(df["time"])
df["datetime"] = df["date"] + df["time"]
df.set_index('datetime',inplace=True)
df = df.resample('W').mean()

#- Estimate seasonal variation
df["weight_kg"] = df["weight"]*0.453592
weight = df["weight_kg"]
weight.ffill(inplace=True)
decomp = sm.tsa.seasonal_decompose(weight,model="additive")

hr = pd.read_hdf("../apple/tmp/training_days.hdf")

#- Plot stuff
sns.set()
fig, (ax0,ax1,ax2) = plt.subplots(nrows=3, ncols=1, constrained_layout=True,sharex=True,gridspec_kw={'height_ratios':[4,1,1]}) 
fig.set_figheight(9)
fig.set_figwidth(10)
ax0.plot(weight.index,weight,c='gray')
ax0.plot(decomp.trend.index,decomp.trend,c='blue')
ax0.set_title("Weight [kg]")
adorne(ax0)

ax1.plot(hr.index,hr,c='gray')
ax1.set_title("Training days per week")
adorne(ax1)
ax1.set(ylim=(0, 7))

ax2.plot(decomp.seasonal.index,decomp.seasonal,c='gray')
ax2.set_title("Estimated seasonal varation [kg]")
adorne(ax2)



#- Annotate text
add_annotation("2017-01-26","No candy, chips or chocolate",(0.4,0.99))
add_annotation("2018-05-15","When do I rest, instead of when do I exercise?",(0.9,0.7))
add_annotation("2019-07-05","No bread",(0.6,0.2))
add_annotation("2019-10-01","No pasta etc",(0.85,0.5))
add_annotation("2019-11-14","No meat",(0.95,0.4))

#plt.show()
plt.savefig("weight.png")





