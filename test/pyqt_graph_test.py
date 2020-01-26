# -*- coding: utf-8 -*-#


import pyqtgraph as pg
import numpy as np
import array
import time
import pandas as pd

from PyQt5.QtCore import QThread, pyqtSignal, QDateTime
from PyQt5.QtWidgets import QWidget, QLineEdit, QListWidget, QPushButton,\
    QVBoxLayout, QLabel

'''
声明线程类
'''


class addItemThread(QThread):
    add_item = pyqtSignal(pd.DataFrame)
    show_time = pyqtSignal(str)

    '''
            添加控件
    '''
    def __init__(self,*args, **kwargs):
        super(addItemThread, self).__init__(*args, **kwargs)
        self.num = 0
        
    def run(self, *args, **kwargs):
        while True:
            df = pd.DataFrame()
            test_dict = {'id':[1,2,3,4,5,6],'name':['Alice','Bob','Cindy','Eric','Helen','Grace '],'math':[90,89,99,78,97,93],'english':[89,94,80,94,94,90]}
            test_dict_df = pd.DataFrame(test_dict)
            print(test_dict_df)
            self.add_item.emit(test_dict_df)
            time.sleep(3)

app = pg.mkQApp()
pg.setConfigOption('background', 'w')
win = pg.GraphicsWindow()
win.setWindowTitle(u'pyqtgraph逐点画波形图')
win.resize(800, 500)

data = array.array('d') #可动态改变数组的大小,double型数组
historyLength = 200

p = win.addPlot()
p.showGrid(x=True, y=True)
#p.setRange(xRange=[0,historyLength], yRange=[-1.2, 1.2], padding=0)
p.setLabel(axis='left', text='y / V')
p.setLabel(axis='bottom', text='x / point')
p.setTitle('y = sin(x)')
p2 = win.addPlot()
#p3 = win.addPlot()

curve = p.plot()
curve2 = p.plot()
idx = 0

def plotData():
    global idx
    tmp = np.sin(np.pi / 50 * idx)
    for i in range(10000000):
        i+=i
    print(i)
    if len(data)<historyLength:
        data.append(tmp)
    else:
        data[:-1] = data[1:]
        data[-1] = tmp
        # curve.setPos(idx-historyLength, 0)
        # p.enableAutoRange('x', True)

    curve.setData(np.frombuffer(data, dtype=np.double))
    # curve.setData(data) #也可以
    idx += 1

# timer = pg.QtCore.QTimer()
# timer.timeout.connect(plotData)
# timer.start(50)

def update(df):
    print(df.dtypes)
    data = np.random.normal(size=1000)
    data2= np.random.normal(size=1000)
    x = np.random.normal(size=1000)
    y = np.random.normal(size=1000)
    #curve.setData(x, y, pen='k', symbol="o",symbolSize=5)
    curve.setData(data,pen='k')
    curve2.setData(data2,pen='r')

at = addItemThread()
at.add_item.connect(update)
at.start()

app.exec_()