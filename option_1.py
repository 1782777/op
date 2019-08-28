import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from optionCalc import BS
import numpy as np
import time
import matplotlib.pyplot as plt
import threading

class Windows(QMainWindow):
    def __init__(self):

        super(Windows, self).__init__()
        self.default_items =[0,0,2.9,0.3,0,0,0,0]
        self.stockPrice =2.963
        self.interestRate =3.75
        self.stockPrice_futrue =2.963
        self.dayLater = 0
        self.currentItem =None

        self.setGeometry(0, 0, 1400, 800)
        self.create_ui()
        self.data= np.zeros((1,8))
        
        

    def create_ui(self):
        wight = QWidget(self)
        wight.setGeometry(10,10,1200,30)
        wight.setStyleSheet('background-color:grey')
        layout_up = QHBoxLayout()
        label = QLabel('认购/认沽（1/-1）')
        layout_up.addWidget(label)
        label2 = QLabel('买入/卖出（1/-1）')
        layout_up.addWidget(label2)
        label3 = QLabel('行权价格')
        layout_up.addWidget(label3)
        label4 = QLabel('期权价格')
        layout_up.addWidget(label4)
        label5 = QLabel('手数')
        layout_up.addWidget(label5)
        label6 = QLabel('距到期天数')
        layout_up.addWidget(label6)
        # label7 = QLabel('计算')
        # layout_up.addWidget(label7)
        label8 = QLabel('隐藏波动率（%）')
        layout_up.addWidget(label8)
        label9 = QLabel('未来波动率（%）')
        layout_up.addWidget(label9)

        wight.setLayout(layout_up)

        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setGeometry(QtCore.QRect(10, 40, 1200, 700))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.itemClicked.connect(self.check_item)
       
        btn_jian = QPushButton(self)
        btn_jian.move(900,740)
        btn_jian.setText('删除')
        btn_jian.clicked.connect(self.del_item)

        btn_jian = QPushButton(self)
        btn_jian.move(1000,740)
        btn_jian.setText('添加')
        btn_jian.clicked.connect(self.add_item)

        wight_r = QWidget(self)
        wight_r.setGeometry(1220,10,140,320)
        #wight_r.setStyleSheet('background-color:grey')
        layout_r = QVBoxLayout()
        labelr_1 =QLabel('50etf当前价格:')
        self.spin_current = QDoubleSpinBox()
        self.spin_current.setDecimals(3)
        self.spin_current.setSingleStep(0.005)
        self.spin_current.setValue(self.stockPrice)
        self.spin_current.valueChanged.connect(lambda val:self.set_stockPrice(val))
        labelr_2 = QLabel('利率')
        self.spin_lilv = QDoubleSpinBox()
        self.spin_lilv.setValue(self.interestRate)
        self.spin_lilv.valueChanged.connect(lambda val:self.set_interestRate(val))
        labelr_3 =QLabel('50etf未来价格:')
        self.spin_future = QDoubleSpinBox()
        self.spin_future.setDecimals(3)
        self.spin_future.setSingleStep(0.005)
        self.spin_future.setValue(self.stockPrice_futrue)
        self.spin_future.valueChanged.connect(lambda val:self.set_stockPriceFutrue(val))

        labelr_daylater =QLabel('几天以后:')
        self.spin_daylater = QSpinBox()
        self.spin_daylater.setValue(self.dayLater)
        self.spin_daylater.valueChanged.connect(lambda val:self.set_daylater(val))

        btn_calculated = QPushButton('计算收益')
        btn_calculated.clicked.connect(self.Show_Profit)
        self.labelr_4 =QLabel('收益')
        btn_draw = QPushButton('画图')
        btn_draw.clicked.connect(self.draw)

        layout_r.addWidget(labelr_1)
        layout_r.addWidget(self.spin_current)
        layout_r.addWidget(labelr_2)
        layout_r.addWidget(self.spin_lilv)
        layout_r.addWidget(labelr_3)
        layout_r.addWidget(self.spin_future)
        layout_r.addWidget(labelr_daylater)
        layout_r.addWidget(self.spin_daylater)
        layout_r.addWidget(btn_calculated)
        layout_r.addWidget(self.labelr_4)
        layout_r.addWidget(btn_draw)

        wight_r.setLayout(layout_r)

        self.statusBar().showMessage('Ready')

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        newAct = QAction('load', self) 
        saveAct = QAction('save', self)  
        fileMenu.addAction(newAct)
        fileMenu.addAction(saveAct)
        fileMenu.triggered[QAction].connect(self.processtrigger)

    def del_item(self):
        if self.currentItem==None:
            return
        index = self.listWidget.row(self.currentItem)
        self.listWidget.takeItem(index)
        

    def add_item(self):
        
        self.make_items(line=self.default_items)

    
        
            

    def processtrigger(self,q):
        #保存和读取
        
        if q.text()=='load':
            fname,_=QFileDialog.getOpenFileName(self,'读取')
            data = np.load(fname)
            self.listWidget.clear()
            self.spin_current.setValue(data[0,0])
            self.spin_lilv.setValue(data[0,2])
            self.spin_future.setValue(data[0,1])
            for i in range(1,data.shape[0]):
                self.make_items(data[i])
            
            
        else:
            filename=QFileDialog.getSaveFileName(self,'save file')
            pub_data = np.zeros((1,8))
            pub_data[0,0] = self.stockPrice
            pub_data[0,1]= self.stockPrice_futrue
            pub_data[0,2] = self.interestRate
            list_data = self.getAllListInfo()
            alldata = np.concatenate((pub_data,list_data),axis=0)
            np.save(filename[0],alldata)


    def make_items(self,line =np.zeros(8)):

        item = QListWidgetItem()
        item.setSizeHint(QSize(1180, 40))
        wight = QWidget()
        layout_main = QHBoxLayout()

        spin_callput = QSpinBox()
        spin_callput.setObjectName('callput')
        spin_callput.setMaximum(1)
        spin_callput.setMinimum(-1)
        spin_callput.setValue(line[0])
        spin_longshort = QSpinBox()
        spin_longshort.setMaximum(1)
        spin_longshort.setMinimum(-1)
        spin_longshort.setValue(line[1])
        spin_longshort.setObjectName('longshort')
        layout_main.addWidget(spin_callput)
        layout_main.addWidget(spin_longshort)

        spin_Eprice = QDoubleSpinBox()
        spin_Eprice.setSingleStep(0.01)
        spin_Eprice.setValue(line[2])
        spin_Eprice.setSingleStep(0.05)
        spin_Eprice.setObjectName('eprice')
        layout_main.addWidget(spin_Eprice)

        spin_price = QDoubleSpinBox()
        spin_price.setDecimals(4)
        spin_price.setValue(line[3])
        spin_price.setSingleStep(0.001)
        spin_price.setObjectName('price')
        layout_main.addWidget(spin_price)

        count = QSpinBox()
        count.setMinimum(0)
        count.setValue(line[4])
        count.setObjectName('count')
        layout_main.addWidget(count)

        times = QSpinBox()
        times.setMinimum(0)
        times.setValue(line[5])
        times.setObjectName('time')
        layout_main.addWidget(times)

        # btm =QPushButton('->')
        # layout_main.addWidget(btm)

        label_iv = QLabel('iv')
        label_iv.setObjectName('iv')
        label_iv.setText(str(line[6]))
        layout_main.addWidget(label_iv)

        iv_h = QDoubleSpinBox()
        iv_h.setMinimum(0)
        iv_h.setValue(line[7])
        iv_h.setObjectName('iv_h')
        layout_main.addWidget(iv_h)

        wight.setLayout(layout_main)
        self.listWidget.addItem(item) 
        self.listWidget.setItemWidget(item, wight) 
        #return wight

    def set_stockPrice(self,v):
        self.stockPrice = v
        self.statusBar().showMessage('当前股价：'+str(v))
        
    def set_interestRate(self,v):
        self.interestRate = v
        self.statusBar().showMessage('当前利率：'+str(v))

    def set_stockPriceFutrue(self,v):
        self.stockPrice_futrue = v
        self.statusBar().showMessage('未来股价：'+str(v))

    def set_daylater(self,v):
        self.dayLater = v
        self.statusBar().showMessage('几天后'+str(v))

    def check_item(self,item):
        
        self.currentItem =item
        callput,longshort,eprice,price,count,time,iv,iv_h = self.get_itemInfo(item)
        if callput==0&longshort==0:
            return
        widget = self.listWidget.itemWidget(item)
        if callput == 1:
            theOption = BS([self.stockPrice,  eprice,  self.interestRate, time],  callPrice = price)
        elif callput == -1:
            theOption = BS([self.stockPrice,  eprice,  self.interestRate, time],  putPrice = price)
        #theOption = BS([2.65,  2.9,  3.75, 5],  callPrice = 0.06)
        impliedVolatility = theOption.impliedVolatility
        #print(impliedVolatility)
        widget.findChild(QLabel,'iv').setText(str(impliedVolatility))
        widget.findChild(QDoubleSpinBox,'iv_h').setValue(impliedVolatility)

    def get_itemInfo(self,item):
        widget = self.listWidget.itemWidget(item)
        callput= widget.findChild(QSpinBox,'callput').value()
        longshort =widget.findChild(QSpinBox,'longshort').value()
        eprice =widget.findChild(QDoubleSpinBox,'eprice').value()
        price =widget.findChild(QDoubleSpinBox,'price').value()
        count =widget.findChild(QSpinBox,'count').value()
        time =widget.findChild(QSpinBox,'time').value()
        iv = widget.findChild(QLabel,'iv').text()
        iv_h =widget.findChild(QDoubleSpinBox,'iv_h').value()
        
        return callput,longshort,eprice,price,count,time,float(iv),iv_h
        
    def getAllListInfo(self):
        
        count =self.listWidget.count()
        data = np.zeros((count,8))
        for j in range(self.listWidget.count()):
            item = self.listWidget.item(j)
            callput,longshort,eprice,price,count,time,iv,iv_h= self.get_itemInfo(item)
            data[j,:]= [callput,longshort,eprice,price,count,time,iv,iv_h]
        return data

    def Calculation_pointMoney(self,pricefuture):
        #print(pricefuture)
        data = self.getAllListInfo()
        alreadPay=0
        price_sametime= 0
        for i in range(0,data.shape[0]):
            alreadPay = alreadPay+data[i,1]*data[i,3]*data[i,4]*10000
            day =data[i,5]-self.dayLater
            if day<1:
                day =1
            futureOption = BS([pricefuture,data[i,2],self.interestRate,day], data[i,7])
            if self.dayLater<data[i,5]:
                if data[i,0] == 1:
                    futureOptionPrice = futureOption.callPrice
                else:
                    futureOptionPrice = futureOption.putPrice
            else:
                print('tianshuchaoguole')
                if data[i,0] == 1:
                    if pricefuture < data[i,2]:
                        futureOptionPrice = 0
                    else:
                        futureOptionPrice = pricefuture -data[i,2]
                else:
                    if pricefuture > data[i,2]:
                        futureOptionPrice = 0
                    else:
                        futureOptionPrice = data[i,2] -pricefuture

            futureOptionPrice =futureOptionPrice*data[i,1]*data[i,4]*10000
            price_sametime= price_sametime+futureOptionPrice
           
        return price_sametime-alreadPay

    def Show_Profit(self):
        profit = self.Calculation_pointMoney(self.stockPrice_futrue)
        #print(profit)
        self.labelr_4.setText(str(profit))
    
    def draw_thread(self):
        t = threading.Thread(target=self.draw)
        t.setDaemon(True) 
        t.start()

    def draw(self):
        longth =np.linspace(-0.2, 0.2, 48)
        profits = np.zeros(longth.shape[0])

        plt.figure(figsize=(16, 7.5))
        ax = plt.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_position(('data', 0))
        x =longth+self.stockPrice_futrue
        for row in range(longth.shape[0]):
            pricefuture =longth[row]+self.stockPrice_futrue
            profits[row] = self.Calculation_pointMoney(pricefuture)
            if row%4==0:
                xx =longth[row]+self.stockPrice_futrue
                plt.annotate("%s" % np.trunc(profits[row]), xy=(xx,profits[row]),xytext=(-20, 10), xycoords='data',textcoords='offset points')
                plt.plot([xx,xx],[0,profits[row]], color ='blue', linewidth=1, linestyle="--")
        y= profits
        
        plt.plot(x ,y,color ='red', linewidth=2.5) 
        plt.show()

    



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    windows = Windows()
    windows.show()
    sys.exit(app.exec_())