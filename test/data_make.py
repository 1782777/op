import numpy as np 
import pandas as pd 
import datetime
import matplotlib.pyplot as plt
import dateutil
import tensorflow as tf
#每天的交易量是成交金额做了累加，每日的交易量是成交量
#v rise v_day rise_d
#yestday可以改一下 现在第一次取值是取的今天开盘价
class data_maker():
    def __init__(self):
        self.pf_min5 = pd.read_excel('data/000016_5min.xlsx',usecols=[0,1, 4,5],skipfooter=1,skiprows=[0,1,3],\
            parse_dates=['      时间'],index_col='      时间')
        self.pf_day = pd.read_excel('data/000016_day.xlsx',usecols=[0,1, 4,5],skipfooter=1,skiprows=[0,1,3],\
            parse_dates=['      时间'],index_col='      时间')
        self.pf_min5.columns=['s','e','v']
        self.pf_day.columns=['s','e','v']
        

        #df_norm = (df - df.min()) / (df.max() - df.min())
    
    def choose_one(self):
        #抽取要个5分钟数据 获得他多日期
        one_monent = self.pf_min5.sample(n=1)
        date = one_monent.index.date
        print(type(one_monent))
        #获得当天所有多五分钟数据
        allday_pd = self.pf_min5[self.pf_min5.index.date==date]
        #获得昨天收盘价格
        start_p =self.pf_day[self.pf_day.index.date==date-\
            dateutil.relativedelta.relativedelta(days=1)].iloc[0,1]
        print(date,start_p)
        #start_p = allday_pd.iloc[0,0]
        #涨跌百分比，做归一化除10
        allday_pd['p']=(allday_pd['e']-start_p)/start_p*10
        pd_allday= allday_pd.drop(['s','e'],axis=1)
        #print(pd_allday)
        
        #取前面48个每天数据
        d_list =self.pf_day[self.pf_day.index.date<date]
        #这里要取多一天，获取前一天的收盘价
        data_day = d_list.tail(48+1)
        #下移动
        data_day['s'] = data_day['e'].shift()
        data_day = data_day.tail(48)
        #print(data_day)
        #合并
        data_day.index = pd_allday.index
        pd_allday['v2'] = data_day['v']
        pd_allday['p2']=(data_day['e']-data_day['s'])/data_day['s']*10
        print(pd_allday)
        pd_allday =pd_allday.drop(['v','v2'],axis=1)
        pd_allday.plot()
        plt.show()

    def _bytes_feature(self,value):
            return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

    def make(self):
        # print(self.pf_min5)
        # print(self.pf_day)
        tfrecords_filename = 'data/train.tfrecords'
        writer = tf.python_io.TFRecordWriter(tfrecords_filename)
        
        #
        last_date = None
        yestoday=None
        for index,row in self.pf_min5.iterrows():
            tmp_df =pd.DataFrame(row).T
            date = tmp_df.index.date
            pd_min_day = self.pf_min5[self.pf_min5.index.date==date]
            if pd_min_day.shape[0]!=48:
                continue
            #昨天多收盘价格q
            if last_date==None:
                last_date=date
            elif last_date!=date:
                yestoday =last_date
                last_date = date
            if yestoday!=None:
                yestoday_end_price =self.pf_day[self.pf_day.index.date==yestoday].iloc[0,1]
            else:
                yestoday_end_price =pd_min_day.iloc[0,0]
            #涨跌百分比
            pd_min_day['rise'] = (pd_min_day['e']-yestoday_end_price)/yestoday_end_price*10
            pd_label = pd_min_day['rise']
            #成交额累加
            pd_min_day['v']=pd_min_day['v'].cumsum(axis=0)
            #取前面48个每天数据
            d_list =self.pf_day[self.pf_day.index.date<date]
            #这里要取多一天，获取前一天的收盘价
            data_day = d_list.tail(48+1)
            #下移动
            data_day['s'] = data_day['e'].shift()
            data_day = data_day.tail(48)
            #data_day['v']=data_day['v'].cumsum(axis=0)
            #把未知数据写0  
            pd_min_day[pd_min_day.index.time >= tmp_df.index.time] =0
            #合并
            data_day.index = pd_min_day.index
            pd_min_day['v_day'] = data_day['v']
            pd_min_day['rise_day']=(data_day['e']-data_day['s'])/data_day['s']*10
            pd_min_day =pd_min_day.drop(['s','e'],axis=1)
            #把未知数据写0  
            
            x = np.array(pd_min_day)
            label = np.array(pd_label)
            print(label.shape)
            example = tf.train.Example(features = tf.train.Features(feature={
                'label' : self._bytes_feature(label.tostring()),
                'x' : self._bytes_feature(x.tostring())
            }))
            writer.write(example.SerializeToString())
        writer.close()

    

    def test_sum(self):
        one_monent = self.pf_min5.sample(n=1)
        date = one_monent.index.date
        pd_allday = self.pf_min5[self.pf_min5.index.date==date]
        pd_day =self.pf_day[self.pf_day.index.date==date]
        print (pd_allday.apply(sum))
        print(pd_day)

    def test(self):
        for index, row in self.pf_min5.iterrows():
            print(index,row)

if __name__ == '__main__':
    pd.set_option('display.width',None)
    dm = data_maker()
    
    dm.make()
    
