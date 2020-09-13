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



#- Plot stuff
sns.set()
fig, (ax0,ax1,ax2) = plt.subplots(nrows=3, ncols=1, constrained_layout=True,sharex=True,gridspec_kw={'height_ratios':[4,1,1]})
fig.set_figheight(9)
fig.set_figwidth(10)
ax0.plot(weight.index,weight,c='gray')
ax0.plot(decomp.trend.index,decomp.trend,c='blue')
ax0.set_title("Weight [kg]")
adorne(ax0)

ax1.plot(decomp.seasonal.index,decomp.seasonal,c='gray')
ax1.set_title("Estimated seasonal varation [kg]")
adorne(ax1)


#- Plot training
hr = pd.read_csv("~/Dropbox/health/strava/2020-09-13/activities.csv")
hr["date"] = pd.to_datetime(hr["Activity Date"])
hr = hr.set_index(pd.DatetimeIndex(hr['date']))

#print(pd.unique(hr["Activity Type"]))

hrt = hr.resample("W-MON").sum()

hrt["Duration"] = hrt["Elapsed Time"]/60/60

ax2.plot(hrt.index,hrt["Duration"],c='gray')
ax2.set_title("Training Hours per week [h]")
adorne(ax2)

hrr = hr[hr["Activity Type"] == "Run"]
hrr = hrr.resample("W-MON").sum()
#hrb = hr[hr["Activity Type"] == "Rock Climb"]

#ax3.plot(hrr.index,hrr["Distance"],c='gray')
#ax3.set_title("Running distance per week [km]")
#adorne(ax3)


#ax1.set(ylim=(0, 7))




#- Annotate text
add_annotation("2017-01-26","No candy, chips or chocolate",(0.4,0.99))
add_annotation("2018-05-15","When do I rest, instead of when do I exercise?",(0.9,0.7))
add_annotation("2019-07-05","No bread",(0.6,0.2))
add_annotation("2019-10-01","No pasta ",(0.85,0.4))
add_annotation("2019-11-14","No meat",(0.95,0.4))
add_annotation("2020-01-10","No snus",(0.90,0.1))
add_annotation("2020-05-26","Meat again",(0.95,0.15))

#plt.show()
plt.savefig("weight.png")





