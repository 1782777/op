from PyQt5.QtWidgets import QPushButton,QWidget,QApplication,QGridLayout,QListWidget,QLineEdit,QVBoxLayout,QLabel
import pyqtgraph as pg
import sys
import numpy as np
from tools import DataModel,HoldPositions
from load_sina import LoadNet
import time
from get_day_histroy import history
import pandas as pd 
from volume import Volume
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime

class addItemThread(QThread):
    update_qvix = pyqtSignal(pd.DataFrame)
    update_north = pyqtSignal(pd.DataFrame)
    update_vol = pyqtSignal(pd.Series,pd.Series)
    update_month = pyqtSignal(pd.DataFrame)
    update_iv =pyqtSignal(pd.DataFrame,pd.DataFrame)
    update_greek = pyqtSignal(list)
    
    def __init__(self,*args, **kwargs):
        super(addItemThread, self).__init__(*args, **kwargs)
        self.data_model =DataModel()
        self.num = 0
        
    def run(self, *args, **kwargs):
        while True:
            df =LoadNet().get_QVIX()
            self.update_qvix.emit(df)

            df_north =LoadNet().get_north()
            self.update_north.emit(df_north)

            df_vol ,cha= Volume().update()
            data ,last = LoadNet().get_50_163()
            ser = (data['current']-last)/last
            self.update_vol.emit(df_vol,ser)
            
            if not self.data_model.df_op.empty:
                df_month = self.data_model.iv_month_50300()
                self.update_month.emit(df_month)

                df_iv50,df_iv300 = self.data_model.get_iv()
                self.update_iv.emit(df_iv50,df_iv300)

                hp = HoldPositions()
                greek = hp.update(self.data_model.df_op)
                self.update_greek.emit(greek)

            time.sleep(3)


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        mthread = addItemThread()
        mthread.update_qvix.connect(self.update_qvix)
        mthread.update_north.connect(self.update_north)
        mthread.update_vol.connect(self.update_volume)
        mthread.update_month.connect(self.update_month)
        mthread.update_iv.connect(self.update_iv)
        mthread.update_greek.connect(self.update_greek)
        mthread.start()
        self.initUI()
        

    def initUI(self):
        self.setGeometry(400,400,1200,620)
        self.setWindowTitle("不被仓位左右思想，没找到弱点不要重仓")
        self.gridLayout = QGridLayout(self)
        self.plot()
        
        '''
        buttom
        '''
        self.label_greek = QLabel('label_greek')
        self.label_greek.setStyleSheet("background-color:rgb(250,250,250)")
        self.gridLayout.addWidget(self.label_greek, 2, 0,1,3)
        '''
        right
        '''
        # wight_r = QWidget(self)
        # layout_r = QVBoxLayout()
        # wight_r.setLayout(layout_r)
        # btn_calculated = QPushButton('计算收益')
        # layout_r.addWidget(btn_calculated)
        # self.gridLayout.addWidget(wight_r, 0, 3,2,1)

    def plot(self):
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        pw_iv50 = pg.PlotWidget(title='50-IV')
        self.plt_iv50_1 = pw_iv50.plot(symbol="o",pen=pg.mkPen("r",width=1),symbolSize=12,symbolBrush=(0,255,0))
        self.plt_iv50_2 = pw_iv50.plot(symbol="o",pen=pg.mkPen("g",width=1),symbolSize=12,symbolBrush=(0,255,0))
        self.plt_iv50_3 = pw_iv50.plot(symbol="o",pen=pg.mkPen("r",width=1),symbolSize=10,symbolBrush=(0,170,0))
        self.plt_iv50_4 = pw_iv50.plot(symbol="o",pen=pg.mkPen("g",width=1),symbolSize=10,symbolBrush=(0,170,0))
        self.plt_iv50_5 = pw_iv50.plot(symbol="o",pen=pg.mkPen("r",width=1),symbolSize=8,symbolBrush=(0,85,0))
        self.plt_iv50_6 = pw_iv50.plot(symbol="o",pen=pg.mkPen("g",width=1),symbolSize=8,symbolBrush=(0,85,0))
        self.plt_iv50_7 = pw_iv50.plot(symbol="o",pen=pg.mkPen("r",width=1),symbolSize=6,symbolBrush=(0,0,0))
        self.plt_iv50_8 = pw_iv50.plot(symbol="o",pen=pg.mkPen("g",width=1),symbolSize=6,symbolBrush=(0,0,0))
        self.gridLayout.addWidget(pw_iv50, 0, 0)
        

        plt300 = pg.PlotWidget(title='300-IV')
        self.plt_iv300_1 = plt300.plot(symbol="o",pen=pg.mkPen("r",width=1),symbolSize=12,symbolBrush=(0,255,0))
        self.plt_iv300_2 = plt300.plot(symbol="o",pen=pg.mkPen("g",width=1),symbolSize=12,symbolBrush=(0,255,0))
        self.plt_iv300_3 = plt300.plot(symbol="o",pen=pg.mkPen("r",width=1),symbolSize=10,symbolBrush=(0,170,0))
        self.plt_iv300_4 = plt300.plot(symbol="o",pen=pg.mkPen("g",width=1),symbolSize=10,symbolBrush=(0,170,0))
        self.plt_iv300_5 = plt300.plot(symbol="o",pen=pg.mkPen("r",width=1),symbolSize=8,symbolBrush=(0,85,0))
        self.plt_iv300_6 = plt300.plot(symbol="o",pen=pg.mkPen("g",width=1),symbolSize=8,symbolBrush=(0,85,0))
        self.plt_iv300_7 = plt300.plot(symbol="o",pen=pg.mkPen("r",width=1),symbolSize=6,symbolBrush=(0,0,0))
        self.plt_iv300_8 = plt300.plot(symbol="o",pen=pg.mkPen("g",width=1),symbolSize=6,symbolBrush=(0,0,0))
        self.gridLayout.addWidget(plt300, 0, 1)

        pw_month = pg.PlotWidget(title='MONTH-50-300-MONTH')
        pw_month.showGrid(x=False,y=True)
        pw_month.addLegend(offset=(30, 100))
        self.plt_month50 = pw_month.plot(name="50")
        self.plt_month300 = pw_month.plot(name="300")
        self.gridLayout.addWidget(pw_month, 0, 2)

        pw_qvix = pg.PlotWidget( title='QVIX')
        pw_qvix.showGrid(x=True,y=True)
        pw_qvix.addLegend()
        self.plt_qvix = pw_qvix.plot(pen=pg.mkPen("d",width=4),name="iv")
        self.gridLayout.addWidget(pw_qvix, 1, 0)

        pw_north = pg.PlotWidget( title='NORTH')
        pw_north.showGrid(x=False,y=True)
        pw_north.addLegend()
        self.plt_north_hgt =pw_north.plot(pen=pg.mkPen("b",width=2),name="hgt")
        self.plt_north_sgt =pw_north.plot(pen=pg.mkPen("g",width=1),name="sgt")
        self.plt_north_all =pw_north.plot(pen=pg.mkPen("d",width=1),name="all")
        self.gridLayout.addWidget(pw_north, 1, 1)

        pw_volume = pg.PlotWidget( title='VOLUME')
        pw_volume.showGrid(x=False,y=True)
        self.plt_volume =pw_volume.plot(name="volume")
        self.stock_50 =pw_volume.plot(name="stock_50")
        self.gridLayout.addWidget(pw_volume, 1, 2)

    def update_qvix(self,df):
        df = df.drop(['Pre','max','min'],axis=1)
        self.plt_qvix.setData(df.index.values, df['QVIX'])

    def update_north(self,df):
        self.plt_north_hgt.setData( df['hgt'].astype(float)/10000)
        self.plt_north_sgt.setData( df['sgt'].astype(float)/10000)
        self.plt_north_all.setData(df['all'].astype(float)/10000)

    def update_volume(self,data,ser):
        self.plt_volume.setPen(pg.mkPen("b",width=3))
        self.plt_volume.setData(data.values)
        self.stock_50.setData(ser)

    def update_month(self,data):
        data.columns=['data','50iv','data2','300iv']
        self.plt_month50.setData(data['50iv'])
        self.plt_month50.setPen(pg.mkPen("r",width=2))
        self.plt_month300.setData(data['300iv'])
        self.plt_month300.setPen(pg.mkPen("b",width=1))

    def update_iv(self,data50,data300):
        data50.sort_index(inplace=True)
        data50 = data50.astype(float)
        data50[data50<1]=np.nan
        self.plt_iv50_1.setData(data50.iloc[:,0])
        self.plt_iv50_2.setData(data50.iloc[:,5])
        self.plt_iv50_3.setData(data50.iloc[:,1])
        self.plt_iv50_4.setData(data50.iloc[:,6])
        self.plt_iv50_5.setData(data50.iloc[:,2])
        self.plt_iv50_6.setData(data50.iloc[:,7])
        self.plt_iv50_7.setData(data50.iloc[:,3])
        self.plt_iv50_8.setData(data50.iloc[:,8])

        data300.sort_index(inplace=True)
        data300 = data300.astype(float)
        data300[data300<1]=np.nan
        self.plt_iv300_1.setData(data300.iloc[:,0])
        self.plt_iv300_2.setData(data300.iloc[:,5])
        self.plt_iv300_3.setData(data300.iloc[:,1])
        self.plt_iv300_4.setData(data300.iloc[:,6])
        self.plt_iv300_5.setData(data300.iloc[:,2])
        self.plt_iv300_6.setData(data300.iloc[:,7])
        self.plt_iv300_7.setData(data300.iloc[:,3])
        self.plt_iv300_8.setData(data300.iloc[:,8])
        
    def update_greek(self,gk):
        text = 'DELTA:{}GAMMA:{}VEGA:{}THETA:{}'.format(gk[0],gk[1],gk[2],gk[3])
        self.label_greek.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())