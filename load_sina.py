import json
import sys
from requests import get
import pandas as pd
import random
import datetime

#'hq.sinajs.cn/list=sh000016'

class LoadNet:
    def __init__(self):
        self.month = self.check_month()
        self.test =0
    
    def check_month(self):
        url='http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getStockName'
        dates = get(url).json()['result']['data']['contractMonth']
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


    def get_op_codes(self,month):
        
        url_up = "http://hq.sinajs.cn/list=OP_UP_510050" + month[-4:]
        print(url_up)
        url_down = "http://hq.sinajs.cn/list=OP_DOWN_510050" + month[-4:]
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

if __name__ == '__main__':
    load = LoadNet()
    print(load.get_sz50_price())
    # month = load.check_month()
    # upcode, downcode= load.get_op_codes(month[0])
    # #print(upcode, downcode)
    # for code in upcode:
    #     pass
    #     print(load.get_op_greek_alphabet(code))
    # day =load.get_op_expire_day(month[0])
    # print(day)
    # print('finish')
