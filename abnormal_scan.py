from load_sina import LoadNet
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from mpl_toolkits.mplot3d import Axes3D

from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


class scan():
    def __init__(self):
        self.load =LoadNet()
        self.months = self.load.check_month()
        self.data_panel = pd.DataFrame()
        
        for month in self.months:
            up ,down = self.load.get_op_codes(month)
            xqj_list =[]
            iv_list=[]
            for code in up:
                data = self.load.get_op_greek_alphabet(code)
                xqj_list.append(float(data[13]))
                iv_list.append(float(data[9]))
            df=pd.DataFrame(iv_list,index=xqj_list,columns=[month+'_购'])
            self.data_panel = pd.concat([self.data_panel,df],axis=1)
            xqj_list =[]
            iv_list=[]
            for code in down:
                data = self.load.get_op_greek_alphabet(code)
                xqj_list.append(float(data[13]))
                iv_list.append(float(data[9]))
            df=pd.DataFrame(iv_list,index=xqj_list,columns=[month+'_沽'])
            self.data_panel = pd.concat([self.data_panel,df],axis=1)
        #data_panel = pd.to_numeric(data_panel)
        self.data_panel.index =pd.to_numeric(self.data_panel.index)
        self.data_panel.columns =[1,2,3,4,5,6,7,8]
        print (self.data_panel)
        # self.data_panel.plot()
        # plt.show()

    def draw(self):
        # x = np.array(self.data_panel.index)
        # y =np.array(self.data_panel.columns)
        x = np.arange(1,7,1)
        print(x)
        
        y = np.arange(1,15,1)
        print(y)
        z = np.array(self.data_panel)
        print(z)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
        fig.colorbar(surf, shrink=0.5, aspect=5)
 
        plt.show()

if __name__ == '__main__':
    s = scan()
    s.draw()
