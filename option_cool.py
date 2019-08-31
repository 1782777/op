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
from load_sina import LoadNet
import sip


class Windows(QMainWindow):
    def __init__(self):
        self.loadsina= LoadNet()
        self.month = self.loadsina.check_month()
        
        self.interestRate=3.75
        self.stockPrice_futrue =2.9
        self.iv_futrue = 20.0
        self.dayLater =0

        super(Windows, self).__init__()
        self.setGeometry(0, 0, 1200, 800)
        self.currentItem =None
        self.create_ui()
        

        self.fill_dayWidget()
        #self.fill_wight_out()
        

    def create_ui(self):
        wight = QWidget(self)
        wight.setGeometry(10,10,1200,30)

        

        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setGeometry(QtCore.QRect(20, 40, 600, 700))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.itemClicked.connect(self.check_in_item)
        
        btn_jian = QPushButton(self)
        btn_jian.move(620,360)
        btn_jian.resize(15,30)
        btn_jian.setText('>')
        btn_jian.clicked.connect(self.del_item)

        

        wight_call = QWidget(self)
        wight_call.setGeometry(635, 70, 100, 670)
        self.layout_call = QVBoxLayout()
        self.layout_call.setContentsMargins(0, 0, 0, 0)
        wight_call.setLayout(self.layout_call)
        
        wight_mid = QWidget(self)
        wight_mid.setGeometry(735, 70, 100, 670)
        
        self.layout_mid = QVBoxLayout()
        self.layout_mid.setContentsMargins(0, 0, 0, 0)
        wight_mid.setLayout(self.layout_mid)
        
        wight_put = QWidget(self)
        wight_put.setGeometry(835, 70, 100, 670)
        self.layout_put = QVBoxLayout()
        self.layout_put.setContentsMargins(0, 0, 0, 0)
        wight_put.setLayout(self.layout_put)
       
        wight_right = QWidget(self)
        wight_right.setGeometry(955, 40, 100, 350)
        #wight_right.setStyleSheet('background-color:gray')
        layout_r = QVBoxLayout()

        self.labelr_currentstock_prince =QLabel()
        self.labelr_currentstock_prince.setText(self.loadsina.get_50etf_price()[3])
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

        labelr_iv_future =QLabel('未来波动:')
        self.spin_future_iv = QDoubleSpinBox()
        self.spin_future_iv.setDecimals(2)
        self.spin_future_iv.setSingleStep(0.05)
        self.spin_future_iv.setValue(self.iv_futrue)
        self.spin_future_iv.valueChanged.connect(lambda val:self.set_ivFuture(val))


        labelr_daylater =QLabel('几天以后:')
        self.spin_daylater = QSpinBox()
        self.spin_daylater.setValue(self.dayLater)
        self.spin_daylater.valueChanged.connect(lambda val:self.set_daylater(val))

        btn_calculated = QPushButton('计算收益')
        btn_calculated.clicked.connect(self.Show_Profit)
        self.labelr_4 =QLabel('收益')
        btn_draw = QPushButton('画图')
        btn_draw.clicked.connect(self.draw)

        layout_r.addWidget(self.labelr_currentstock_prince)
        layout_r.addWidget(labelr_2)
        layout_r.addWidget(self.spin_lilv)
        layout_r.addWidget(labelr_3)
        layout_r.addWidget(self.spin_future)
        layout_r.addWidget(labelr_iv_future)
        layout_r.addWidget(self.spin_future_iv)
        layout_r.addWidget(labelr_daylater)
        layout_r.addWidget(self.spin_daylater)
        layout_r.addWidget(btn_calculated)
        layout_r.addWidget(self.labelr_4)
        layout_r.addWidget(btn_draw)
        wight_right.setLayout(layout_r)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        newAct = QAction('load', self) 
        saveAct = QAction('save', self)  
        fileMenu.addAction(newAct)
        fileMenu.addAction(saveAct)
        fileMenu.triggered[QAction].connect(self.processtrigger)

    def rest(self):
        pass

    def processtrigger(self,q):
        #保存和读取
        
        if q.text()=='load':
            fname,_=QFileDialog.getOpenFileName(self,'读取')
            data = np.load(fname)
            print(data)
            self.listWidget.clear()
            for i in range(0,data.shape[0]):
                code = str(data[i,0])[0:8]
                ls =data[i,1]
                count = data[i,2]
                self.add_listwidget(code,lonshort=ls,count=count)
            
            
        else:
            filename=QFileDialog.getSaveFileName(self,'save file')
            count =self.listWidget.count()
            data = np.zeros((count,3))
            
            for j in range(self.listWidget.count()):
                item = self.listWidget.item(j)
                code,ls,count =self.get_itemInfo(item)
                data[j,:]=[code,ls,count]
            print (data)
            np.save(filename[0],data)

    def set_interestRate(self,value):
        pass
    
    def set_stockPriceFutrue(self,value):
        self.stockPrice_futrue =value

    def set_ivFuture(self,value):
        self.iv_futrue = value

    def set_daylater(self,value):
        self.dayLater = value

    def Show_Profit(self):
        pass

    def draw(self):
        pass

    def fill_dayWidget(self):
        # for i in self.layout_call.count():
        #     self.layout_call.remove(self.layout_call.children().at(i)i)
        
        

        wight_out_tt =QWidget(self)
        wight_out_tt.setGeometry(635, 40, 300, 25)
        layout_out_tt = QHBoxLayout()
        layout_out_tt.setContentsMargins(0, 0, 0, 0)
        #wight_out_tt.setStyleSheet('background-color:red')
        for month in self.month:
            btm = QPushButton(month) 
            btm.clicked.connect(self.on_monthbtm_click)
            layout_out_tt.addWidget(btm)
        wight_out_tt.setLayout(layout_out_tt)

    def check_in_item(self,item):
        self.currentItem =item
        self.get_itemInfo(item)
    
    def check_out_item(self):
        pass

    def on_monthbtm_click(self):
        btm =self.sender() 
        month = btm.text()
        print(month)
        self.fill_wight_out(month)

    def fill_wight_out(self,month):
        for i in range(self.layout_call.count()): 
            self.layout_call.itemAt(i).widget().deleteLater()
        for i in range(self.layout_mid.count()): 
            self.layout_mid.itemAt(i).widget().deleteLater()
        for i in range(self.layout_put.count()): 
            self.layout_put.itemAt(i).widget().deleteLater()

        
        callop,putop = self.loadsina.get_op_codes(month)
        for op in callop:
            opprice = self.loadsina.get_op_info(op)
            btm = QPushButton(opprice[2])
            btm.setObjectName(op)
            btm.clicked.connect(self.outBtm_click)  
            
            self.layout_call.addWidget(btm)
        for op in callop:
            opprice = self.loadsina.get_op_info(op)
            btm = QPushButton(opprice[37][-4:])
            btm.setEnabled(False)
            self.layout_mid.addWidget(btm)

        for op in putop:
            opprice = self.loadsina.get_op_info(op)
            btm = QPushButton(opprice[2])
            btm.setObjectName(op)
            btm.clicked.connect(self.outBtm_click) 
            self.layout_put.addWidget(btm)
    
    def outBtm_click(self):
        btm =self.sender() 
        print(btm.objectName())
        self.add_listwidget(btm.objectName())

    def add_listwidget(self,opcode,lonshort=0,count=0):
        print('addlist_opcode:::'+opcode)
        greek = self.loadsina.get_op_greek_alphabet(opcode)
        print(greek)
        data ='20'+greek[12][7:11]
        expire_day = self.loadsina.get_op_expire_day(data)[1]
        

        item = QListWidgetItem()
        item.setToolTip(opcode)
        item.setSizeHint(QSize(600, 40))
        wight = QWidget()
        layout_main = QHBoxLayout()

        # label_code = QLabel('id')
        # label_code.setText(opcode)
        # layout_main.addWidget(label_code)

        spin_longshort = QSpinBox()
        spin_longshort.setMaximum(1)
        spin_longshort.setMinimum(-1)
        spin_longshort.setValue(lonshort)
        spin_longshort.setObjectName('longshort')
        layout_main.addWidget(spin_longshort)

        label_callput = QLabel('callput')
        label_callput.setObjectName('callput')
        label_callput.setText(greek[0][5])
        layout_main.addWidget(label_callput)

        label_eprice = QLabel('eprice')
        label_eprice.setObjectName('eprice')
        label_eprice.setText(greek[13])
        layout_main.addWidget(label_eprice)

        label_price = QLabel('price')
        label_price.setObjectName('price')
        label_price.setText(greek[14])
        layout_main.addWidget(label_price)

        Delta = QLabel('Delta')
        Delta.setText(greek[5])
        layout_main.addWidget(Delta)
        Gamma = QLabel('Gamma')
        Gamma.setText(greek[6])
        layout_main.addWidget(Gamma)
        Theta = QLabel('Theta')
        Theta.setText(greek[7])
        layout_main.addWidget(Theta)
        Vega = QLabel('Vega')
        Vega.setText(greek[8])
        layout_main.addWidget(Vega)
        iv = QLabel('iv')
        iv.setObjectName('iv')
        iv.setText(greek[9])
        layout_main.addWidget(iv)

        spin_count = QSpinBox()
        spin_count.setMinimum(0)
        spin_count.setValue(count)
        spin_count.setObjectName('count')
        layout_main.addWidget(spin_count)

        label_expire_day = QLabel('label_expire_day')
        label_expire_day.setObjectName('label_expire_day')
        label_expire_day.setText(str(expire_day))
        layout_main.addWidget(label_expire_day)


        wight.setLayout(layout_main)
        self.listWidget.addItem(item) 
        self.listWidget.setItemWidget(item, wight) 
    
    def del_item(self):
        if self.currentItem==None:
            return
        index = self.listWidget.row(self.currentItem)
        self.listWidget.takeItem(index)

    def get_itemInfo(self,item):
        widget = self.listWidget.itemWidget(item)
        code = item.toolTip()
        longshort =widget.findChild(QSpinBox,'longshort').value()
        count =widget.findChild(QSpinBox,'count').value()
        
        callput_text =widget.findChild(QLabel,'callput').text()
        callput=0
        if callput_text=='购':
            callput=1
        else:
            callput = -1
        eprice =widget.findChild(QLabel,'eprice').text()
        price =widget.findChild(QLabel,'price').text()
        time =widget.findChild(QLabel,'label_expire_day').text()
        iv =widget.findChild(QLabel,'iv').text()
        iv_h=self.iv_futrue
        #print (code,callput,longshort,eprice,price,count,time,iv,iv_h)
        return code,callput,longshort,eprice,price,count,time,iv,iv_h

    def getAllListInfo(self):
        count =self.listWidget.count()
        data = np.zeros((count,8))
        for j in range(self.listWidget.count()):
            item = self.listWidget.item(j)
            code,callput,longshort,eprice,price,count,time,iv,iv_h= self.get_itemInfo(item)
            data[j,:]= [callput,longshort,eprice,price,count,time,iv,iv_h]
        return data

    def Calculation_pointMoney(self,pricefuture):
        
        #print(pricefuture)
        data = self.getAllListInfo()
        print(data)
        alreadPay=0
        price_sametime= 0
        for i in range(0,data.shape[0]):
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

            
            
            if True:
                alreadPay = alreadPay+data[i,1]*data[i,3]*data[i,4]*10000
                futureOptionPrice =futureOptionPrice*data[i,1]*data[i,4]*10000
            else:
                futureOptionPrice =0

            price_sametime= price_sametime+futureOptionPrice
           
        return price_sametime-alreadPay

    def Show_Profit(self):
        profit = self.Calculation_pointMoney(self.stockPrice_futrue)
        #print(profit)
        self.labelr_4.setText(str(profit))

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