from load_sina import LoadNet
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from mpl_toolkits.mplot3d import Axes3D

from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

offset_real =0.05  #小于或者大于多少算实值
offset =0.80 #偏差

class scan():
    def __init__(self):
        self.load =LoadNet()
        self.months = self.load.check_month()
        # self.data_panel = pd.DataFrame()
        # self.fig = plt.figure()
        # self.tmp =0.0
        # self.ax = self.fig.gca(projection='3d')
        # timer = self.fig.canvas.new_timer(interval=1000)
        # timer.add_callback(self.draw)
        # timer.start()
        # plt.show()

    def get_df_price(self):
        data_panel = pd.DataFrame()
        for month in self.months:
            up ,down = self.load.get_op_codes(month)
            xqj_list =[]
            iv_list=[]
            for code in up:
                data = self.load.get_op_greek_alphabet(code)
                xqj_list.append(float(data[13]))
                iv_list.append(float(data[14]))
            df=pd.DataFrame(iv_list,index=xqj_list,columns=[month])
            data_panel = pd.concat([data_panel,df],axis=1)
            xqj_list =[]
            iv_list=[]
            for code in down:
                data = self.load.get_op_greek_alphabet(code)
                xqj_list.append(float(data[13]))
                iv_list.append(float(data[14]))
            df=pd.DataFrame(iv_list,index=xqj_list,columns=[month])
            data_panel = pd.concat([data_panel,df],axis=1)
        #print (data_panel)
        return data_panel

    def check_deep_real_value(self,df_data):
        etf_price = float(self.load.get_50etf_price()[3])
        etf_price_up =etf_price-etf_price*offset_real
        etf_price_down =etf_price+etf_price*offset_real
        #print(etf_price)

        df_data.columns =[1,-1,1,-1,1,-1,1,-1]
        real_value_up = df_data[df_data.index<etf_price_up][[1]]
        real_value_down =df_data[df_data.index>etf_price_down][[-1]]
        real_value_up = etf_price -real_value_up
        real_value_down =etf_price +real_value_down
        # print(real_value_up)
        #print(real_value_down)
        for index, row in real_value_up.iterrows():
            row.index = self.months
            if(len(row[row/index<offset].index)>0):
                print(index,str(row[row/index<offset].index[0]),'购----------')
        for index, row in real_value_down.iterrows():
            row.index = self.months
            #print(row[row/index])
            if(len(row[row/index>2-offset].index)>0):
                print(index,str(row[row/index>2-offset].index[0]),'沽---------')
        #print('====================================================')

    def draw(self):
        self.data_panel = pd.DataFrame()
        for month in self.months:
            up ,down = self.load.get_op_codes(month)
            xqj_list =[]
            iv_list=[]
            for code in up:
                data = self.load.get_op_greek_alphabet(code)
                xqj_list.append(float(data[13]))
                iv_list.append(float(data[9]))
            df=pd.DataFrame(iv_list,index=xqj_list,columns=[month])
            self.data_panel = pd.concat([self.data_panel,df],axis=1)
            xqj_list =[]
            iv_list=[]
            for code in down:
                data = self.load.get_op_greek_alphabet(code)
                xqj_list.append(float(data[13]))
                iv_list.append(float(data[9]))
            df=pd.DataFrame(iv_list,index=xqj_list,columns=[month])
            self.data_panel = pd.concat([self.data_panel,df],axis=1)
        
        self.data_panel.index =pd.to_numeric(self.data_panel.index)
        self.data_panel.columns =[1,2,3,4,5,6,7,8]
        print (self.data_panel)

        x = np.array(self.data_panel.index)
        y =np.array(self.data_panel.columns)
       
        X,Y =np.meshgrid(y,x)
        print(X.shape,Y.shape)
        Z = np.array(self.data_panel)
        self.tmp =self.tmp+0.2
        Z[5,5] =self.tmp
        # fig = plt.figure()
        # ax = fig.gca(projection='3d')
        surf = self.ax.plot_surface(X, Y, Z,rcount=100, ccount=100, cmap=cm.coolwarm, edgecolor='green')
        self.ax.figure.canvas.draw()
        
        

    def testShow(self):
        theta = 2 * np.pi * np.random.random(1000)
        r = 6 * np.random.random(1000)
        x = np.ravel(r * np.sin(theta))
        y = np.ravel(r * np.cos(theta))
        z = np.sin(np.sqrt(x ** 2 + y ** 2))
        ax = plt.axes(projection='3d')
        ax.scatter(x, y, z, c=z, cmap='viridis', linewidth=0.5)
        plt.show()
        

if __name__ == '__main__':
    s = scan()
    i= 500
    while True:
        if(i%500==0):
            print('持续检测深度实值合约价差>20%')
        s.check_deep_real_value(s.get_df_price())
        i+=i

    

   
