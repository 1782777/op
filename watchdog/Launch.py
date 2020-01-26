
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from get_day_histroy import history
import matplotlib.font_manager as font_manager
from load_sina import LoadNet
import time
import threading
from tools import DataModel
from tools import HoldPositions
from volume import Volume

class Test:
    def __init__(self):
        self.UPDATE_TIME =10000
        self.model = DataModel()
        self.v = Volume()

        self.hold_positions = HoldPositions()
        self.colors = ['r','orange','darkgreen','k']
        #plt.ion()
        self.fig = plt.figure(facecolor='darkgray',figsize=(19,10))
        plt.tight_layout(pad=1, w_pad=1.0, h_pad=1.0) 
        self.ax_iv50 = self.fig.add_subplot(231)
        self.ax_iv300 = self.fig.add_subplot(232)
        self.ax_iv_month = self.fig.add_subplot(233)
        self.ax_volume =self.fig.add_subplot(236)
        self.ax_greek =self.fig.add_subplot(235)
        self.ax_QVIX =self.fig.add_subplot(234)

        # t= threading.Thread(target=self.loop)
        # t.start()

        timer = self.fig.canvas.new_timer(interval=self.UPDATE_TIME)
        timer.add_callback(self.loop)
        timer.start()
        plt.show()

    def loop(self):
        print('test') 
        df = self.model.df_op 
        if not df.empty:
                self.draw_iv()
                self.draw_iv_month()
                self.draw_volume50()
                self.draw_greek()
                self.draw_qvix()
        plt.tight_layout(pad=1, w_pad=1.0, h_pad=1.0) 
        self.fig.canvas.draw()

    def draw_iv(self):
        print ('draw_iv')
        self.ax_iv50.cla()
        self.ax_iv300.cla()
        
        self.ax_iv50.set_ylim([1, 50])
        self.ax_iv300.set_ylim([1, 50])
        
        
        iv_50,iv_300 = self.model.get_iv() 
        print ('draw_iv_finish')
        #print(iv_50)
        iv_50 =iv_50.astype(float)
        iv_300 = iv_300.astype(float)

        columns= iv_50.columns.values
        #plt.xticks(iv_50['x'].iloc[0].values)
        for i in range(0,4):
            #print(columns[i])
            iv_50.plot.scatter(x='x',y=columns[i],alpha=0.5,color =self.colors[i],ax=self.ax_iv50)
        self.ax_iv50.set(xlabel='',ylabel='',title='IV-50')
        self.ax_iv50.grid()
        
        columns= iv_300.columns.values
        for i in range(0,4):
            #print(columns[i])
            iv_300.plot.scatter(x='x',y=columns[i],alpha=0.5,color =self.colors[i],ax=self.ax_iv300)
        self.ax_iv300.set(xlabel='',ylabel='',title='IV-300') 
        self.ax_iv300.grid()

    def draw_iv_month(self):
        self.ax_iv_month.cla()
        self.ax_iv_month.set_ylim(10,35)
        self.ax_iv_month.set_yticks([10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,35])
        print('draw_iv_month')
        data = self.model.iv_month_50300() 
        #print(data)
        print('draw_iv_month_finish')
        test = data.plot(ax=self.ax_iv_month,color=['r','b'])
        #print(type(test))
        #ax2 = test.twiny()
        self.ax_iv_month.legend(['50','300'],loc='upper right')
        self.ax_iv_month.set(xlabel='',ylabel='',title='50-MEAN-300')
        self.ax_iv_month.grid()
        

    def draw_volume50(self):
        print ('draw_volume')
        self.ax_volume.cla()
        
        data,cha = self.v.update()
        self.ax_volume.plot(data,'b,-',label=cha)
        self.ax_volume.legend([cha],loc='lower center')
        #self.ax_volume.text(0,0,"111",fontsize = 25)
        print ('draw_volume_finish')
        '''
        new volume
        '''


    def draw_greek(self):
        self.ax_greek.cla()
        greek = self.hold_positions.update(self.model.df_op)
        delta ='delta:'+str(greek[0])
        gamma ='gamma:'+str(greek[1])
        vega = 'vega:'+str(greek[2])
        theta ='theta:'+str(greek[3])
        print(delta,gamma,vega,theta)
        self.ax_greek.text(0.2,0.7,'delta:'+str(greek[0]),fontsize=12,style='italic',color='mediumvioletred')
        self.ax_greek.text(0.2,0.6,'gamma:'+str(greek[1]),fontsize=12,style='italic',color='mediumvioletred')
        self.ax_greek.text(0.2,0.5,'vega:'+str(greek[2]),fontsize=12,style='italic',color='mediumvioletred')
        self.ax_greek.text(0.2,0.4,'theta:'+str(greek[3]),fontsize=12,style='italic',color='mediumvioletred')

    def draw_qvix(self):
        self.ax_QVIX.cla()
        #print (LoadNet().get_QVIX())
        df =LoadNet().get_QVIX()
        # iv = df['QVIX'].astype(float)
        # time =df.index.values
        # print(iv,time)
        # self.ax_QVIX.plot(time,iv)
        pd.to_datetime(df['Time'])
        df.index = df['Time']
        #print(df.columns)
        df = df.drop(['Time','Pre','max','min'],axis=1)
        df.plot(ax=self.ax_QVIX)

t=Test()