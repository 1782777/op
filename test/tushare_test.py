import tushare as ts
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class tush():
    def __init__(self):
        ts.set_token('cab985c55c4477461541810292d52e90887d94103dd9defebb4270cf')
        self.pro = ts.pro_api()

    def get_50_day(self):
        df =ts.get_hist_data('sz50')
        lastday = df['close'].shift(-1)
        df['lastday']= lastday
        
        openhigh = (df['open']-df['lastday'])/df['lastday']*100
        
        df['open_high'] = openhigh.shift(-1)
        
        
        df = df.drop(columns=['v_ma20','ma10','ma20','v_ma5','v_ma10','ma5','price_change','high','low','open','close','lastday'], axis=1)
        df.index = pd.to_datetime(df.index)
        print(df)
        # p_price = df['p_change'].shift(1)
        # df['p_change']= p_price
        # print(df)

        return df

    def get_north_money(self):
        df = self.pro.moneyflow_hsgt(start_date='20170101', end_date='20190908')
        
        date = pd.to_datetime(df['trade_date'])
        df.index = date
        data = df['north_money']
        
        return data
        # tarde_date = df['trade_date']
        # df.index = tarde_date.to_datetime()
        # print (df["north_money"])

if __name__ == '__main__':
    tss = tush()
    df_sh = tss.get_50_day()
    df_north = tss.get_north_money()
    result = pd.concat([df_north, df_sh], axis=1, join='inner')
    #print(result)
    result['north_money'] = result['north_money']/result['north_money'].max()*4
    result['volume'] = result['volume']/result['volume'].max()*6-1
    #result['p_change'] = result['p_change']/result['p_change'].max()
    result['open_high'] = result['open_high']/result['open_high'].max()

    result= result.drop(columns=['open_high','volume'], axis=1)
    #print(result)
    # df_norm = (result - result.min()) / (result.max() - result.min())
    #result.plot(kind='bar')
    result.plot()
    plt.grid(linestyle='-.')
    plt.show()

