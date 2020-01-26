import json
import sys
from requests import get
import pandas as pd
import random
import datetime
import matplotlib.pyplot as plt

#'hq.sinajs.cn/list=sh000016'

class LoadNet:
    def __init__(self):
        self.month = self.check_month()
        self.test =0
    
    def check_month(self):
        url='http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getStockName'
        needTry = True
        while needTry:
            try:
                dates = get(url).json()['result']['data']['contractMonth']
                needTry = False
            except:
                needTry = True
        return [''.join(i.split('-')) for i in dates][1:]

    def get_op_expire_day(self,date):
        url = "http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getRemainderDay?date={date}01"
        needTry = True
        while needTry:
            try:
                data = get(url.format(date=date)).json()['result']['data']
                needTry = False
            except:
                needTry = True
        #data = get(url.format(date=date)).json()['result']['data']
        return data['expireDay'], data['remainderDays']


    def get_op_codes(self,num,month):
        
        url_up = "http://hq.sinajs.cn/list=OP_UP_"+num + month[-4:]
        print(url_up)
        url_down = "http://hq.sinajs.cn/list=OP_DOWN_"+num + month[-4:]
        needTry = True
        while needTry:
            try:
                data_up = str(get(url_up).content).replace('"', ',').split(',')
                needTry = False
            except:
                needTry = True
        #data_up = str(get(url_up).content).replace('"', ',').split(',')
        codes_up = [i[7:] for i in data_up if i.startswith('CON_OP_')]
        needTry = True
        while needTry:
            try:
                data_down = str(get(url_down).content).replace('"', ',').split(',')
                needTry = False
            except:
                needTry = True
        #data_down = str(get(url_down).content).replace('"', ',').split(',')
        codes_down = [i[7:] for i in data_down if i.startswith('CON_OP_')]
        return codes_up, codes_down

    def get_allop_codes(self,month):
        codes =[]
        name = ""
        for mon in month:
            name += "OP_UP_510050" + mon[-4:] +","
            name += "OP_DOWN_510050"+ mon[-4:] +","
            name += "OP_UP_510300"+ mon[-4:] +","
            name += "OP_DOWN_510300"+ mon[-4:] +","
        url = "http://hq.sinajs.cn/list=" + name
        #print(url)
        needTry = True
        while needTry:
            try:
                data = str(get(url).content)
                needTry = False
            except:
                needTry = True
        lines = data.split(';')
        for line in lines:
            word = line.replace('"', ',').split(',')
            for i in word:
                if i.startswith('CON_OP_'):
                    #print(i)
                    codes.append(i)
        return codes
        
    
    def get_op_info(self,code):
        url = "http://hq.sinajs.cn/list=CON_OP_{code}".format(code=code)
        data = get(url).content.decode('gbk')
        data = data[data.find('"') + 1: data.rfind('"')].split(',')
        # fields = ['买量', '买价', '最新价', '卖价', '卖量', '持仓量', '涨幅', '行权价', '昨收价', '开盘价', '涨停价',
        #           '跌停价', '申卖价五', '申卖量五', '申卖价四', '申卖量四', '申卖价三', '申卖量三', '申卖价二',
        #           '申卖量二', '申卖价一', '申卖量一', '申买价一', '申买量一 ', '申买价二', '申买量二', '申买价三',
        #           '申买量三', '申买价四', '申买量四', '申买价五', '申买量五', '行情时间', '主力合约标识', '状态码',
        #           '标的证券类型', '标的股票', '期权合约简称', '振幅', '最高价', '最低价', '成交量', '成交额']
        #result = list(zip(fields, data))
        return data

    def get_allop_info(self,codes):
        name = ""
        for code in codes:
            name += code + ","
        url = "http://hq.sinajs.cn/list=" + name
        
        names,prices,eprices,edays,days=[],[],[],[],[]
        needTry = True
        while needTry:
            try:
                data = get(url).content.decode('gbk')
                needTry = False
            except:
                needTry = True
        lines = data.split(';')
        for line in lines:
            word = line[data.find('"') + 1: data.rfind('"')].split(',')
            #print(word)
            if len(word)>1:
                names.append(word[37])
                prices.append(word[2])
                eprices.append(word[7])
                edays.append(word[46])
                days.append(word[47])
        # fields = ['买量', '买价', '最新价', '卖价', '卖量', '持仓量', '涨幅', '行权价', '昨收价', '开盘价', '涨停价',
        #           '跌停价', '申卖价五', '申卖量五', '申卖价四', '申卖量四', '申卖价三', '申卖量三', '申卖价二',
        #           '申卖量二', '申卖价一', '申卖量一', '申买价一', '申买量一 ', '申买价二', '申买量二', '申买价三',
        #           '申买量三', '申买价四', '申买量四', '申买价五', '申买量五', '行情时间', '主力合约标识', '状态码',
        #           '标的证券类型', '标的股票', '期权合约简称', '振幅', '最高价', '最低价', '成交量', '成交额']
        #result = list(zip(fields, data))
        return codes,names,prices,eprices,edays,days

    def get_op_greek_alphabet(self,code):
        url = "http://hq.sinajs.cn/list=CON_SO_{code}".format(code=code)
        needTry = True
        while needTry:
            try:
                data = get(url).content.decode('gbk')
                needTry = False
            except:
                needTry = True

        #data = get(url).content.decode('gbk')
        data = data[data.find('"') + 1: data.rfind('"')].split(',')
        # fields = ['期权合约简称', '成交量', 'Delta', 'Gamma', 'Theta', 'Vega', '隐含波动率', '最高价', '最低价', '交易代码',
        #         '行权价', '最新价', '理论价值']
        # return list(zip(fields, [data[0]] + data[4:]))
        #return data[4:]
        return data
    
    def get_50etf_price(self):
        url = "http://hq.sinajs.cn/list=sh510050"
        needTry = True
        while needTry:
            try:
                data = get(url).content.decode('gbk')
                needTry = False
            except:
                needTry = True
        #data = get(url).content.decode('gbk')
        data = data[data.find('"') + 1: data.rfind('"')].split(',')
        fields = ['股票名字', '今日开盘价', '昨日收盘价', '当前价格', '今日最高价', '今日最低价', '竞买价', '竞卖价',
                '成交的股票数', '成交金额', '买一量', '买一价', '买二量', '买二价', '买三量', '买三价', '买四量', '买四价',
                '买五量', '买五价', '卖一量', '卖一价', '卖二量', '卖二价', '卖三量', '卖三价', '卖四量', '卖四价',
                '卖五量', '卖五价', '日期', '时间']
        #return list(zip(fields, data))
        return data

    def get_300etf_price(self):
        url = "http://hq.sinajs.cn/list=sh510300"
        needTry = True
        while needTry:
            try:
                data = get(url).content.decode('gbk')
                needTry = False
            except:
                needTry = True
        #data = get(url).content.decode('gbk')
        data = data[data.find('"') + 1: data.rfind('"')].split(',')
        fields = ['股票名字', '今日开盘价', '昨日收盘价', '当前价格', '今日最高价', '今日最低价', '竞买价', '竞卖价',
                '成交的股票数', '成交金额', '买一量', '买一价', '买二量', '买二价', '买三量', '买三价', '买四量', '买四价',
                '买五量', '买五价', '卖一量', '卖一价', '卖二量', '卖二价', '卖三量', '卖三价', '卖四量', '卖四价',
                '卖五量', '卖五价', '日期', '时间']
        #return list(zip(fields, data))
        return data

    def get_sz50_price(self):
        url = "http://hq.sinajs.cn/list=sh000016"
        needTry = True
        while needTry:
            try:
                data = get(url).content.decode('gbk')
                needTry = False
            except:
                needTry = True
        data = data[data.find('"') + 1: data.rfind('"')].split(',')
        fields = ['股票名字', '今日开盘价', '昨日收盘价', '当前价格', '今日最高价', '今日最低价', '竞买价', '竞卖价',
                '成交的股票数', '成交金额', '买一量', '买一价', '买二量', '买二价', '买三量', '买三价', '买四量', '买四价',
                '买五量', '买五价', '卖一量', '卖一价', '卖二量', '卖二价', '卖三量', '卖三价', '卖四量', '卖四价',
                '卖五量', '卖五价', '日期', '时间']
        #return list(zip(fields, data))
        return data

    def get_sz300_price(self):
        url = "http://hq.sinajs.cn/list=sh000300"
        needTry = True
        while needTry:
            try:
                data = get(url).content.decode('gbk')
                needTry = False
            except:
                needTry = True
        data = data[data.find('"') + 1: data.rfind('"')].split(',')
        fields = ['股票名字', '今日开盘价', '昨日收盘价', '当前价格', '今日最高价', '今日最低价', '竞买价', '竞卖价',
                '成交的股票数', '成交金额', '买一量', '买一价', '买二量', '买二价', '买三量', '买三价', '买四量', '买四价',
                '买五量', '买五价', '卖一量', '卖一价', '卖二量', '卖二价', '卖三量', '卖三价', '卖四量', '卖四价',
                '卖五量', '卖五价', '日期', '时间']
        #return list(zip(fields, data))
        return data

    def get_test(self):
        date = pd.datetime.now()+datetime.timedelta(hours=-10,minutes=2.4)
        str_date = date.strftime('%H:%M:%S')
        self.test = self.test+random.randint(1000,2200)
        str_vol = str(self.test)
        print(str_date,str_vol)
        fields = ['股票名字', '今日开盘价', '昨日收盘价', '当前价格', '今日最高价', '今日最低价', '竞买价', '竞卖价',
                str_vol, '成交金额', '买一量', '买一价', '买二量', '买二价', '买三量', '买三价', '买四量', '买四价',
                '买五量', '买五价', '卖一量', '卖一价', '卖二量', '卖二价', '卖三量', '卖三价', '卖四量', '卖四价',
                '卖五量', '卖五价', '日期', str_date]
        return fields


    def get_50_163(self):
        url ='http://img1.money.126.net/data/hs/time/today/0000016.json'
        datas = get(url).json()['data']
        df = pd.DataFrame(datas,columns=['time','current','no','volume'])
        df['time'].astype(int)
        df.index = df['time']
        df = df.drop(['time','no'],axis=1)
        last_price = get(url).json()['yestclose']
        return df,last_price

    def get_50_5days_163(self):
        url ='http://img1.money.126.net/data/hs/time/4days/0000016.json'
        datas = get(url).json()['data']
        df_all = pd.DataFrame()
        for data in datas:
            d = data['data']
            df = pd.DataFrame(d,columns=['time','current','no','volume'])
            print(d)
            print('===========================================================================================')
            df_all = df_all+df
        return df_all

    def get_north(self):
        url ='http://push2.eastmoney.com/api/qt/kamt.rtmin/get?fields1=f1&fields2=f51,f52,f54,f56&ut=b2884a393a59ad64002292a3e90d46a5'
        datas = get(url).json()['data']['s2n']
        all=[]
        for data in datas:
            line = data.split(',')
            all.append(line)
        df = pd.DataFrame(all,columns=['time','sgt','hgt','all'])
        return df

    def get_QVIX(self):
        url ='http://1.optbbs.com/d/csv/d/data.csv'
        needTry = True
        while needTry:
            try:
                df = pd.read_csv(url)
                needTry = False
            except:
                needTry = True
        return df

if __name__ == '__main__':
    load = LoadNet()
    data ,last = load.get_50_163()
    print ((data['current']-last)/last,last)
    # data['current'].plot(subplots=True)
    # data['volume'].plot(kind='area',secondary_y=['volume'],subplots=True)
    # plt.show()
    

    # datas =load.get_50_5days_163()
    # print(datas)
    
