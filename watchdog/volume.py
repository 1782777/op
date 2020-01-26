import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from get_day_histroy import history
import matplotlib.font_manager as font_manager
from load_sina import LoadNet
import threading

class Volume:
    def __init__(self):
        pd.options.display.max_rows = None
        his=history()
        self.mean_data = his.get_dayMean()
        #self.a =LoadNet().get_sz50_price()
        self.mean_data['current']=0
        self.mean_data['mean']=0
        self.diff_data =pd.DataFrame()

        self.res = pd.DataFrame()
        self.cha = 0.0

        # t= threading.Thread(target=self.update)
        # t.start()

    def update(self):
        #ax.cla()
        a =LoadNet().get_sz50_price()
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
        self.mean_data.loc[self.mean_data.index>time.time(),'current'] = int(str_volume)/10000
        
        self.diff_data = self.mean_data.copy()
        self.diff_data['current'] = pd.to_numeric(self.diff_data['current']) 
        self.diff_data['current'] = self.diff_data['current'].diff(1)
        self.diff_data.iloc[0,1] =float( self.mean_data.iloc[0,1])
        self.mean_data['mean']=self.mean_data['current']/self.mean_data['VOL-TDX.VOLUME']
        self.cha=(current-tomorrow)/tomorrow*100
        self.res = self.mean_data['mean'][self.mean_data.index<=time_end.time()]
        return self.mean_data['mean'][self.mean_data.index<=time_end.time()],self.cha
        #print(self.mean_data)
        #ax.plot(self.mean_data['mean'][self.mean_data.index<=time_end.time()],'b,-')
    
    def get_line_cha(self):
        return self.res,self.cha
    
if __name__ =='__main__':
    vol = Volume()
    info,cp = vol.update()
    print(info.dtypes,cp)