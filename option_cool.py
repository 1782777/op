import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from optionCalc import BS, Me
import numpy as np
import time
import matplotlib.pyplot as plt
import threading
from load_sina import LoadNet
import sip
import pandas as pd

#YEAR_DAY = 243.0
YEAR_DAY = 365.0

class Option(object):
    """期权类"""
    def __init__(self, stockPrice = 3.000, strikePrice = 3.00, interestRate = 3.00, daysToExpiration = 20, callput =1, optionPrice = 0.0500, impliedVolatility = None):
        self.stockPrice = stockPrice
        self.strikePrice = strikePrice
        self.interestRate = interestRate
        dayRate = YEAR_DAY/365
        if daysToExpiration==0: daysToExpiration =0.5
        self.daysToExpiration = daysToExpiration * dayRate
        self.callput = callput
        if impliedVolatility == None:
            self.optionPrice = optionPrice
            self.getVolatility()
            self.calcGreek()
        else:
            self.impliedVolatility = impliedVolatility
            self.calcGreek1()

        
    def getVolatility(self):
        currentOption = None
        if self.callput ==1:
            currentOption = BS([self.stockPrice, self.strikePrice, self.interestRate, self.daysToExpiration], callPrice=self.optionPrice)
        else:
            currentOption = BS([self.stockPrice, self.strikePrice, self.interestRate, self.daysToExpiration], putPrice=self.optionPrice)
        self.impliedVolatility = currentOption.impliedVolatility

    def calcGreek(self):
        currentOption = BS([self.stockPrice, self.strikePrice, self.interestRate, self.daysToExpiration], volatility = self.impliedVolatility)

        self.delta = currentOption.callDelta
        if self.callput == -1:
            self.delta = currentOption.putDelta

        self.gamma = currentOption.gamma

        self.theta = currentOption.callTheta
        if self.callput == -1:
            self.theta = currentOption.putTheta

        self.vega = currentOption.vega

        self.currentOption = currentOption

    def calcGreek1(self):    #事先不知道optionPrice
        self.calcGreek()
        currentOption = self.currentOption
        self.optionPrice = currentOption.callPrice
        if self.callput == -1:
            self.optionPrice = currentOption.putPrice


class Windows(QMainWindow):
    def __init__(self):
        self.loadsina= LoadNet()
        self.month = self.loadsina.check_month()
        
        self.interestRate=3.00
        self.stockPrice = float(self.loadsina.get_50etf_price()[3])
        self.stockPrice_future = self.stockPrice
        self.iv_future = 0
        self.dayLater =0

        super(Windows, self).__init__()
        self.setGeometry(20, 50, 1800, 1200)
        self.currentItem =None
        self.create_ui()
        

        self.fill_dayWidget()
        #self.fill_wight_out()
        

    def create_ui(self):
        wight = QWidget(self)
        wight.setGeometry(10,10,1400,300)

        

        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setGeometry(QtCore.QRect(20, 40, 1000, 1000))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.itemClicked.connect(self.check_in_item)
        
        btn_jian = QPushButton(self)
        btn_jian.move(1020,360)
        btn_jian.resize(15,30)
        btn_jian.setText('>')
        btn_jian.clicked.connect(self.del_item)
        
        

        wight_call = QWidget(self)
        wight_call.setGeometry(1035, 70, 100, 670)
        self.layout_call = QVBoxLayout()
        self.layout_call.setContentsMargins(0, 0, 0, 0)
        wight_call.setLayout(self.layout_call)
        
        wight_mid = QWidget(self)
        wight_mid.setGeometry(1135, 70, 100, 670)
        
        self.layout_mid = QVBoxLayout()
        self.layout_mid.setContentsMargins(0, 0, 0, 0)
        wight_mid.setLayout(self.layout_mid)
        
        wight_put = QWidget(self)
        wight_put.setGeometry(1235, 70, 100, 670)
        self.layout_put = QVBoxLayout()
        self.layout_put.setContentsMargins(0, 0, 0, 0)
        wight_put.setLayout(self.layout_put)
       
        wight_right = QWidget(self)
        wight_right.setGeometry(1355, 40, 200, 650)
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
        self.spin_future.setValue(float(self.labelr_currentstock_prince.text()))
        self.spin_future.valueChanged.connect(lambda val:self.set_stockPricefuture(val))

        labelr_iv_future =QLabel('未来波动:')
        # self.spin_future_iv = QDoubleSpinBox()
        # self.spin_future_iv.setDecimals(2)
        # self.spin_future_iv.setSingleStep(0.05)
        # self.spin_future_iv.setValue(self.iv_future)
        #self.spin_future_iv.valueChanged.connect(lambda val:self.set_ivFuture(val))
        self.sp=QSlider(Qt.Horizontal)
        self.sp.setMinimum(-100)
        self.sp.setMaximum(100)
        self.sp.setSingleStep(0.01)
        self.sp.setValue(self.iv_future)
        self.sp.setTickPosition(QSlider.TicksBelow)
        self.sp.setTickInterval(5)
        self.sp.valueChanged.connect(lambda val:self.set_ivFuture(val))


        labelr_daylater =QLabel('几天以后:')
        self.spin_daylater = QSpinBox()
        self.spin_daylater.setRange(0,300)
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
        layout_r.addWidget(self.sp)
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
        csvAct = QAction('load_csv', self)
        fileMenu.addAction(newAct)
        fileMenu.addAction(saveAct)
        fileMenu.addAction(csvAct)
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
            
            
        elif q.text()=='save':
            filename=QFileDialog.getSaveFileName(self,'save file')
            count =self.listWidget.count()
            data = np.zeros((count,3))
            
            for j in range(self.listWidget.count()):
                item = self.listWidget.item(j)
                code,callput,longshort,eprice,price,count,time,iv,iv_h =self.get_itemInfo(item)
                data[j,:]=[code,longshort,count]
            #print (data)
            np.save(filename[0],data)
        
        else:
            fname,_=QFileDialog.getOpenFileName(self,'读取')
            csv_data = pd.read_csv(fname, usecols=['代码', '买卖', '持仓'], encoding='GB2312')
            
            positionList = csv_data.values.tolist()
            print(positionList)

            self.listWidget.clear()
            for option in positionList:
                code = str(option[0])
                bs = option[1]
                if bs == '买':
                    ls = 1
                else:
                    ls = -1
                count = option[2]
                self.add_listwidget(code,lonshort=ls,count=count)         

    def set_interestRate(self,value):
        self.interestRate = value
    
    def set_stockPricefuture(self,value):
        self.stockPrice_future =value

    def set_ivFuture(self,value):
        print(value)
        self.iv_future = value

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
        wight_out_tt.setGeometry(1035, 40, 300, 25)
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
        #data表示是几月的合约
        
        expire_day = self.loadsina.get_op_expire_day(data)[1]
        
        callput_text = greek[0][5]   #“购”或“沽”

        eprice = greek[13]      #行权价，如c2.95

        price = greek[14]       #当前期权价格

        callput = 1
        if callput_text=='购':
            callput=1
        else:
            callput = -1
        
        currentOption = Option(stockPrice=self.stockPrice, strikePrice = float(eprice), interestRate=self.interestRate, daysToExpiration=float(expire_day), callput = callput, optionPrice=float(price))

        impliedVolatility = currentOption.impliedVolatility

        #print(impliedVolatility,"iv_")

        #iv_h=impliedVolatility+ self.iv_future*impliedVolatility*0.01
        #print(iv_h,"iv_h")

        delta = currentOption.delta

        gamma = currentOption.gamma

        theta = currentOption.theta

        vega = currentOption.vega

        item = QListWidgetItem()
        item.setToolTip(opcode)
        item.setSizeHint(QSize(600, 60))
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
        label_callput.setText(callput_text)
        
        layout_main.addWidget(label_callput)

        label_eprice = QLabel('eprice')
        label_eprice.setObjectName('eprice')
        label_eprice.setText(eprice)
        layout_main.addWidget(label_eprice)

        label_price = QLabel('price')
        label_price.setObjectName('price')
        label_price.setText(price)
        layout_main.addWidget(label_price)

        Delta = QLabel('Delta')
        Delta.setText(str(delta)[0:5])
        layout_main.addWidget(Delta)
        Gamma = QLabel('Gamma')
        Gamma.setText(str(gamma)[0:5])
        layout_main.addWidget(Gamma)
        Theta = QLabel('Theta')
        Theta.setText(str(theta)[0:8])
        layout_main.addWidget(Theta)
        Vega = QLabel('Vega')
        Vega.setText(str(vega)[0:8])
        layout_main.addWidget(Vega)
        iv = QLabel('iv')
        iv.setObjectName('iv')
        iv_value = round(impliedVolatility,4)
        iv.setText(str(iv_value)[0:5])
        #iv.setText(greek[9])
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
        expire_day =widget.findChild(QLabel,'label_expire_day').text()
        #iv =widget.findChild(QLabel,'iv').text()

        currentOption = Option(stockPrice=self.stockPrice, strikePrice = float(eprice), interestRate=self.interestRate, daysToExpiration=float(expire_day), callput = callput, optionPrice=float(price))

        impliedVolatility = currentOption.impliedVolatility

        iv_h=impliedVolatility+ self.iv_future*impliedVolatility*0.01

        return code,callput,longshort,eprice,price,count,expire_day,impliedVolatility,iv_h

    def getAllListInfo(self):
        count =self.listWidget.count()
        data = np.zeros((count,8))
        for j in range(self.listWidget.count()):
            item = self.listWidget.item(j)
            code,callput,longshort,eprice,price,count,time,iv,iv_h= self.get_itemInfo(item)
            data[j,:]= [callput,longshort,eprice,price,count,time,iv,iv_h]
        return data

    def Calculation_pointMoney(self,pricefuture,iscal_greeks= False):
        
        #print(pricefuture)
        data = self.getAllListInfo()
        #print(data)
        alreadPay=0
        price_sametime= 0
        delta =0
        gamma=0
        vega=0
        theta=0

        
        for i in range(0,data.shape[0]):
            #data[i,5]是合约距到期有多少天
            expire_day = data[i,5]
            #day表示以新的日期算，距到期还有多少天
            day =expire_day-self.dayLater

            #print('data? ',data)

            callput = data[i,0]

            strikePrice = data[i,2]

            longShort = data[i,1]

            optionPrice = data[i,3]

            amount = data[i,4] 
            
            new_iv = data[i,7]

            if day<1:
                day = 1

            futureOption = Option(stockPrice = pricefuture, strikePrice=strikePrice, interestRate=self.interestRate, daysToExpiration=day, callput=callput, impliedVolatility=new_iv)
          
            

            if self.dayLater < expire_day:
                futureOptionPrice = futureOption.optionPrice
                if iscal_greeks:
                    delta = amount*longShort*futureOption.delta+delta
                    print("futureOption.delta=", futureOption.delta)
                    print("delta=",delta)
                    gamma = amount*longShort*futureOption.gamma+gamma
                    vega = amount*longShort*futureOption.vega+vega
                    theta = amount*longShort*futureOption.theta+theta 

            else:
                print('tianshuchaoguole')
                if callput == 1:
                    if pricefuture < strikePrice:
                        futureOptionPrice = 0
                    else:
                        futureOptionPrice = pricefuture -strikePrice
                else:
                    if pricefuture > strikePrice:
                        futureOptionPrice = 0
                    else:
                        futureOptionPrice = strikePrice -pricefuture

            
            
            if True:
                alreadPay = alreadPay+longShort*optionPrice*amount*10000
                futureOptionPrice = longShort*futureOptionPrice*amount*10000

            else:
                futureOptionPrice =0

            price_sametime= price_sametime+futureOptionPrice
        if iscal_greeks:
            print(delta,gamma,vega,theta)
            self.statusBar().showMessage('delta='+str(delta)+'  gamma='+str(gamma)+'  vega='+str(vega)+'  theta='+str(theta))
        
        return price_sametime-alreadPay

    def Show_Profit(self):
        profit = self.Calculation_pointMoney(self.stockPrice_future,iscal_greeks=True)
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
        #x =longth+self.stockPrice_future
        x =longth+self.stockPrice
        
        for row in range(longth.shape[0]):
            #pricefuture =longth[row]+self.stockPrice_future
            pricefuture =longth[row]+self.stockPrice
            profits[row] = self.Calculation_pointMoney(pricefuture)
            if row%4==0:
                #xx =longth[row]+self.stockPrice_future
                xx =longth[row]+self.stockPrice
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
