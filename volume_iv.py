import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from get_day_histroy import history
import matplotlib.font_manager as font_manager
from load_sina import LoadNet

class IV:
    def __init__(self,ln):
        self.ln = ln
    def get_all_iv(self):
        mouths = ln.check_month()
        print (mouths)




pd.options.display.max_rows = None
his=history()
mean_data = his.get_dayMean()
ln= LoadNet()

mean_data['current']=0
mean_data['mean']=0


#fig, ax = plt.subplots()
fig = plt.figure(facecolor='darkgray')
ax = fig.add_subplot(414)
ax_50_mouth = fig.add_subplot(421)
ax_50_each = fig.add_subplot(422)
ax_300_mouth = fig.add_subplot(423)
ax_300_each =  fig.add_subplot(424)
ax_300_50 =  fig.add_subplot(413)


ax.legend(loc='upper center', ncol=4, prop=font_manager.FontProperties(size=8))

#diff_data =pd.DataFrame()
def sin_output(ax):
    ax.cla()
    
    

    

    a = ln.get_sz50_price()
    #a.cumsum(axis=0)
    str_time =a[31]
    str_time_end ="15:00:00"
    str_volume =a[9]
    tomorrow = float(a[2])
    current = float(a[3])
    #print(str_time,str_volume)
    time =pd.datetime.strptime(str_time,'%H:%M:%S')
    min_1 = pd.Timedelta(minutes=1)
    time_end =time + min_1
    
    #mean_data['current'][mean_data.index>time.time()] = int(str_volume)/10000
    mean_data.loc[mean_data.index>time.time(),'current'] = int(str_volume)/10000
    
    diff_data = mean_data.copy()
    diff_data['current'] = pd.to_numeric(diff_data['current']) 
    diff_data['current'] = diff_data['current'].diff(1)
    diff_data.iloc[0,1] =float( mean_data.iloc[0,1])
    mean_data['mean']=mean_data['current']/mean_data['VOL-TDX.VOLUME']

    #print(mean_data)
    ax.plot(mean_data['mean'][mean_data.index<=time_end.time()],'b,-')
    
    cha=(current-tomorrow)/tomorrow*100
    color_label ='r'
    if cha<0: color_label='g'
    ax.set_title(format(cha, '.2f'),color=color_label)

    ax.figure.canvas.draw()
 
 
# timer = fig.canvas.new_timer(interval=5000)
# timer.add_callback(sin_output, ax)
# timer.start()
# plt.show()

iv = IV(ln)
iv.get_all_iv()
