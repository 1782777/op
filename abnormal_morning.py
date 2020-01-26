from load_sina import LoadNet
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from mpl_toolkits.mplot3d import Axes3D

from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sip
import sys
import time
from optionCalc import BS,Me

offset_real =0.01 #小于或者大于多少算实值
offset =0.96#偏差


class scan():
    def __init__(self):
        self.load =LoadNet()
        self.months = self.load.check_month()
        self.day_later =self.load.get_op_expire_day('2019')
        print(self.day_later)
        self.etf_price =2.95
        self.data_price=pd.DataFrame()
        self.data_iv =pd.DataFrame()
        self.histroy_high =300
        # self.data_panel = pd.DataFrame()
        # self.fig = plt.figure()
        # self.tmp =0.0
        # self.ax = self.fig.gca(projection='3d')
        # timer = self.fig.canvas.new_timer(interval=1000)
        # timer.add_callback(self.draw)
        # timer.start()
        # plt.show()

    def get_df(self):
        self.etf_price = float(self.load.get_50etf_price()[3])
        self.data_price=pd.DataFrame()
        self.data_iv =pd.DataFrame()
        for month in self.months:
            date, time =self.load.get_op_expire_day(month)
            up ,down = self.load.get_op_codes(month)
            xqj_list =[]
            iv_list =[]
            p_list=[]
            for code in up:
                data = self.load.get_op_info(code)
                xqj_list.append(float(data[7]))
                p_list.append(float(data[1]))
                # theOption = BS([self.etf_price, float(data[7]) ,3.75, time],  callPrice = data[1])
                # iv_list.append(theOption.impliedVolatility)
            df_p=pd.DataFrame(p_list,index=xqj_list,columns=[month+'_call'])
            self.data_price= pd.concat([self.data_price,df_p],axis=1)
            df_iv = pd.DataFrame(iv_list,index=xqj_list,columns=[month+'_call'])
            self.data_iv =pd.concat([self.data_iv,df_iv],axis=1)
            xqj_list =[]
            iv_list =[]
            p_list=[]
            for code in down:
                data = self.load.get_op_info(code)
                xqj_list.append(float(data[7]))
                p_list.append(float(data[1]))
                # theOption = BS([self.etf_price, float(data[7]) ,3.75, time],  putPrice = data[1])
                # iv_list.append(theOption.impliedVolatility)
            df_p=pd.DataFrame(p_list,index=xqj_list,columns=[month+'_put'])
            self.data_price= pd.concat([self.data_price,df_p],axis=1)
            df_iv = pd.DataFrame(iv_list,index=xqj_list,columns=[month+'_put'])
            self.data_iv =pd.concat([self.data_iv,df_iv],axis=1)
        self.data_price = self.data_price[self.data_price!=0]
        self.data_iv = self.data_iv[self.data_iv!=0]
        print(self.data_price)
        #print(self.data_iv) 

    def find_pd_diff(self):
        df_diff = pd.DataFrame()#期权价格偏离 越大越偏离便宜 只适用于实值
        for month in self.months:
            #列出看涨现货差价
            long_diff =self.etf_price - \
                (self.data_price.index + self.data_price[month+'_call'])
            df_diff[month+'call_p'] =long_diff
            short_diff =self.data_price.index - \
                (self.etf_price + self.data_price[month+'_put'])
            df_diff[month+'put_p'] =short_diff

        for index, row in df_diff.iterrows():
            for i,v in row.items():
                if v >0.01:
                    print(df_diff)
        return df_diff
        

    # def find_most_cheapset(self,data):
    #     cheapest_op =data.idxmax()
    #     most_op =data.idxmin()
    #     print(cheapest_op,most_op)

    def find_combination_pd(self):
        #买一个现货赚多少钱 卖一个现货赚-多少钱
        pd_combination = pd.DataFrame()
        for month in self.months:
            
            good_price =self.data_price[month+'_call']- self.data_price[month+'_put']\
                -(self.etf_price-self.data_price.index)
            pd_combination[month]=-good_price*10000
            
        #print(pd_combination)
        return pd_combination

    def find_good_combination(self,pd_data):
        # short_ = pd_data[pd_data.columns].min()
        # long_ = pd_data[pd_data.columns].max()
        # print(long_,short_)
        # money = long_ - short_
        long_=0
        short_=0
        money=1
        long_date='none'
        short_data='none'
        long_right=0
        short_right=0
        for index, row in pd_data.iterrows():
            for i, v in row.items():
                if(v>long_):
                    long_=v
                    long_date =i
                    long_right=index
                if(v<short_):
                    short_=v
                    short_data=i
                    short_right=index
        money = long_ - short_
        long_ =("%.1f" % long_)
        short_ =("%.1f" % short_)
        #money=("%.1f" % money)
        return long_date,long_right,long_,short_data,short_right,short_,money
    
    def get_histroy_high(self,h):
        if h>self.histroy_high:
            self.histroy_high = h
        return self.histroy_high

    def save_excel(self):
        data = QDateTime.currentDateTime()
        currTime = data.toString("yyyy-MM-dd-hh-mm-ss")
        writer = pd.ExcelWriter('./save_file/'+currTime+'.xlsx')
        self.data_price.to_excel(writer,sheet_name='price')
        self.data_iv.to_excel(writer,sheet_name='iv')
        self.find_combination_pd().to_excel(writer,sheet_name='longshort')
        writer.save()
    # def draw(self):
    #     self.data_panel = pd.DataFrame()
    #     for month in self.months:
    #         up ,down = self.load.get_op_codes(month)
    #         xqj_list =[]
    #         iv_list=[]
    #         for code in up:
    #             data = self.load.get_op_greek_alphabet(code)
    #             xqj_list.append(float(data[13]))
    #             iv_list.append(float(data[9]))
    #         df=pd.DataFrame(iv_list,index=xqj_list,columns=[month])
    #         self.data_panel = pd.concat([self.data_panel,df],axis=1)
    #         xqj_list =[]
    #         iv_list=[]
    #         for code in down:
    #             data = self.load.get_op_greek_alphabet(code)
    #             xqj_list.append(float(data[13]))
    #             iv_list.append(float(data[9]))
    #         df=pd.DataFrame(iv_list,index=xqj_list,columns=[month])
    #         self.data_panel = pd.concat([self.data_panel,df],axis=1)
        
    #     self.data_panel.index =pd.to_numeric(self.data_panel.index)
    #     self.data_panel.columns =[1,2,3,4,5,6,7,8]
    #     print (self.data_panel)

    #     x = np.array(self.data_panel.index)
    #     y =np.array(self.data_panel.columns)
       
    #     X,Y =np.meshgrid(y,x)
    #     print(X.shape,Y.shape)
    #     Z = np.array(self.data_panel)
        
    #     surf = self.ax.plot_surface(X, Y, Z,rcount=100, ccount=100, cmap=cm.coolwarm, edgecolor='green')
    #     self.ax.figure.canvas.draw()
    
class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(20, 50, 1360, 600)

        wight = QWidget(self)
        wight.setGeometry(0,0,680,30)
        #wight.setStyleSheet('background-color:orange')
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.label_long = QLabel('最好的做多现货组合')
        layout.addWidget(self.label_long)
        self.label_short = QLabel('最好的做空现货组合')
        layout.addWidget(self.label_short)
        self.label_combination = QLabel('组合收益')
        layout.addWidget(self.label_combination)
        self.btm_save = QPushButton('save',wight)
        self.btm_save.clicked.connect(self.save_data)
        self.label_histroy_high = QLabel('最高纪录')
        layout.addWidget(self.btm_save)
        layout.addWidget(self.label_histroy_high)
        wight.setLayout(layout)
        #tabel
        wight_2 = QWidget(self)
        wight_2.setGeometry(0,40,540,620)
        wight_2.setStyleSheet('background-color:grey')
        layout2 = QHBoxLayout()
        layout2.setContentsMargins(0, 0, 0, 0)
        self.myTable=QTableView(wight_2)
        wight_3 = QWidget(self)
        wight_3.setGeometry(540,40,1140,620)
        layout3 = QHBoxLayout()
        layout3.setContentsMargins(0, 0, 0, 0)
        self.myTable_iv=QTableView(wight_3)
        #self.myTable.resizeColumnsToContents()
        layout2.addWidget(self.myTable)
        layout3.addWidget(self.myTable_iv)
        wight_2.setLayout(layout2)
        wight_3.setLayout(layout3)


         # 创建线程
        self.backend = BackendThread()
        # 连接信号
        self.backend.update_date.connect(self.set_label)
        self.backend.update_tabel.connect(self.set_tabel)
        self.backend.update_tabel_iv.connect(self.set_tabel_iv)
        self.backend.update_histroy_high.connect(self.set_label_histroy)
        self.thread = QThread()
        self.backend.moveToThread(self.thread)
        # 开始线程
        self.thread.started.connect(self.backend.run)
        self.thread.start()

    def set_label(self,long_date,long_right,long_,short_data,short_right,short_,money):        
        self.label_long.setText(long_date+'  '+long_right+'  '+long_)
        self.label_short.setText(short_data+'  '+short_right+'  '+short_)
        self.label_combination.setText(money)
        if float(money)>300:
             self.label_combination.setStyleSheet("background-color:rgb(180,80,40)")
        elif float(money)>500:
             self.label_combination.setStyleSheet("background-color:gold")
        if float(long_)>250:
             self.label_long.setStyleSheet("background-color:rgb(190,60,59)")
        if float(short_)<-250:
             self.label_short.setStyleSheet("background-color:rgb(50,200,50)")

    def set_tabel(self,data):
        #print(data)
        self.myTable.setModel(self.pd_to_model(data,factor=0.6))
    
    def set_tabel_iv(self,data):
        #print(data)
        self.myTable_iv.setModel(self.pd_to_model(data,factor=5))

    def set_label_histroy(self,money):
        self.label_histroy_high.setText('最高:'+str(money))

    def pd_to_model(self,pd_data,factor):
        model = QtGui.QStandardItemModel()
        model.setRowCount(pd_data.shape[0]) 
        model.setColumnCount(pd_data.shape[1]) 
        model.setHorizontalHeaderLabels(pd_data.columns)
        model.setVerticalHeaderLabels(pd_data.index.astype(str))
        data_np = pd_data.values
        data_np = np.around(data_np, decimals=2)
        data_str =data_np.astype(str)
        for i in range(data_str.shape[0]):
            for j in range(data_str.shape[1]):
                item =QtGui.QStandardItem(data_str[i,j])
                r =0
                g =0
                if np.isnan(data_np[i,j])==False:
                    tmp = int(data_np[i,j]*factor)
                    if(tmp>0):
                        r=min(tmp,225)
                        g=0
                    if(tmp<0):
                        r=0
                        g=min(-tmp,225)
                item.setBackground(QBrush(QColor(r, g, 0)))
                item.setForeground(QBrush(QColor(120, 170, 220)))
                model.setItem(i,j,item)
        return model

    def save_data(self):
        self.backend.s.save_excel()

class BackendThread(QObject):
    # 通过类成员对象定义信号
    def __init__(self):
        super(BackendThread,self).__init__() 
        self.s = scan()

    update_date = pyqtSignal(str,str,str,str,str,str,str)
    update_tabel =pyqtSignal(pd.DataFrame)
    update_tabel_iv =pyqtSignal(pd.DataFrame)
    update_histroy_high =pyqtSignal(float)
    
    # 处理业务逻辑
    def run(self):
        while True:
            # data = QDateTime.currentDateTime()
            # currTime = data.toString("yyyy-MM-dd hh:mm:ss")
            
            self.s.get_df()
            combination_pd = self.s.find_combination_pd()
            long_date,long_right,long_,short_data,short_right,short_,money =\
                 self.s.find_good_combination(combination_pd)
            self.update_date.emit(long_date,str(long_right),\
                str(long_),short_data,str(short_right),str(short_),"%.1f" % money)
            self.update_histroy_high.emit(self.s.get_histroy_high(money))
            if money>400:
                self.s.save_excel()
            self.s.find_pd_diff()
            self.update_tabel.emit(combination_pd)
            self.update_tabel_iv.emit(self.s.data_iv)
            time.sleep(0.1)
            


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
    
    # s = scan()
    # s.get_df()
    # s.find_pd_diff()
    # s.find_combination_pd()
    # s.save_excel()
    

   
