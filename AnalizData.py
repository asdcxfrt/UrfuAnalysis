import os
import pandas as pd
import Analiz
from datetime import datetime
import seaborn as sns
import threading
import matplotlib.pyplot as plt
import pylab
files=os.listdir("Data/")
Dates=list(map(lambda x:x.split("_")[1:],files))
Dates=list(map(lambda x:"_".join(x),Dates))
Dates=list(map(lambda x:x.replace(".csv",""),Dates))
Dates=sorted(Dates, key=lambda d: datetime.strptime(d, "%d-%m-%Y_%H-%M-%S"))

sns.set(rc = {'figure.figsize':(20,20)})
colors = sns.color_palette("Set3", 7)
f = plt.figure(figsize=(6, 6))
gs = f.add_gridspec(2, 2)

dfB=pd.DataFrame()
dfG=pd.DataFrame()
df100=pd.DataFrame()
def Prepare(Date):
    global dfB,dfG,df1
    df=pd.read_csv(f"Data/dataURFU_{Date}.csv")
    rez=Analiz.DataProc(df)
    dfB["Направление"]=rez["Направление"]
    dfG["Направление"]=rez["Направление"]
    df100["Направление"]=rez["Направление"]
    dfB[Date]=rez["Лучше меня"]
    dfG[Date]=rez["Зеленых лучше меня"]
    df100[Date]=rez["Балл 100ого"]


for Date in Dates:
    print(Date)
    Prepare(Date)


dfB = dfB.reindex(columns=["Направление"]+Dates)
dfG = dfG.reindex(columns=["Направление"]+Dates)
df100 = df100.reindex(columns=["Направление"]+Dates)

def Plot(DF,id):
    df = pd.DataFrame({"Date": DF.iloc[id].keys()[1:],
                       "Value": DF.iloc[id].values[1:]})
    df=df.set_index("Date")

    p=sns.lineplot(data=df,
        y=DF.iloc[id].values[1:],x=DF.iloc[id].keys()[1:],
        palette ='coolwarm')
    p.tick_params(axis='x', rotation=90)
plt.subplot(2, 2, 1)
for i in range(0,7):
    Plot(dfB,i)
plt.subplot(2, 2, 2)
for i in range(0,7):
    Plot(dfG,i)

plt.subplot(2, 2, 3)
for i in range(0,7):
    Plot(df100,i)
plt.legend(labels=dfB["Направление"],loc='lower right',bbox_to_anchor=(2, 0))

plt.show()
