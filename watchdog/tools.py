import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from get_day_histroy import history
import matplotlib.font_manager as font_manager
from load_sina import LoadNet
import random
from optionCalc import BS
import time
import threading

YEAR_DAY = 365.0
INTERESTRate =3.0
RATE=3
pd.options.display.max_rows = None

class Option(object):
    """期权类"""
    def __init__(self, stockPrice = 3.000, strikePrice = 3.00, interestRate = 3.00, daysToExpiration = 20, callput =1, optionPrice = 0.0500, impliedVolatility = None):
        self.stockPrice = stockPrice
        self.strikePrice = strikePrice
        self.interestRate = interestRate
        dayRate = YEAR_DAY/365
        if daysToExpiration==0: daysToExpiration=0.5
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

class DataModel:
    def __init__(self):
        self.ln = LoadNet()
        
        self.stock_info_50 = self.ln.get_sz50_price()
        self.stock_info_300 = self.ln.get_sz300_price()
        self.stock_price_50etf  = 0.0
        self.stock_price_300etf= 0.0
        self.df_op =pd.DataFrame()
        
        self.df_codes = self.init_allcodes()

        
        t= threading.Thread(target=self.loop)
        t.start()
        

    def init_allcodes(self):
        mouths = self.ln.check_month()
        codes = self.ln.get_allop_codes(mouths)
        return codes

    def update_alldf(self):
        '''
        get 50etf 300etf
        '''
        stock_price_50_allinfo = self.ln.get_50etf_price()
        time = stock_price_50_allinfo[31]
        self.stock_price_50etf = stock_price_50_allinfo[3]
        self.stock_price_300etf = self.ln.get_300etf_price()[3]
        self.stock_info_50 = self.ln.get_sz50_price()
        self.stock_info_300 = self.ln.get_sz300_price()

        '''
        get sina info all
        '''
        codes,names,prices,eprices,edays,days = self.ln.get_allop_info(self.df_codes)
        df_all = pd.DataFrame()
        df_all['code'] =codes
        df_all['name'] =names
        df_all['price'] =prices
        df_all['eprice'] =eprices
        df_all['eday'] =edays
        df_all['day'] =days


        '''
        get my count discountlist
        '''
        discountlist =[]
        for date, row in df_all.T.iteritems():
            discount =0
            if  '50ETF购' in row['name']:
                discount = float(self.stock_price_50etf) - float(row['eprice']) - float(row['price'])
            if  '50ETF沽' in row['name']:
                discount = float(row['eprice']) - float(self.stock_price_50etf) -  float(row['price'])
            if  '300ETF购' in row['name']:
                discount = float(self.stock_price_300etf) - float(row['eprice']) - float(row['price'])
            if  '300ETF沽' in row['name']:
                discount = float(row['eprice']) - float(self.stock_price_300etf) -  float(row['price'])  
            
            discountlist.append(discount)
        df_all['discount']=discountlist
        
        '''
        count iv
        '''
        ivlist=[]
        deltalist=[] 
        gammalist = []
        thetalist = []
        vegalist=[]
        timelist=[]
        
        for date, row in df_all.T.iteritems(): 
            
            if row['day'] == 0.0:
                impliedVolatility = 0
                delta = 0
                gamma = 0
                theta = 0
                vega = 0
                #row['price'] = float(row['price'])  + discount*1.5
            else:
                op_price = float(row['price']) 
                eprice = float(row['eprice'])
                day = float(row['day'])

                callput =1
                if '沽' in row['name']:
                    callput =-1

                stock_price = self.stock_price_50etf
                if '300ETF' in row['name']:
                    stock_price = self.stock_price_300etf
                #print (stock_price,eprice,INTERESTRate,day,callput,op_price)
                currentOption = Option(stockPrice= stock_price, strikePrice = eprice, interestRate=INTERESTRate, daysToExpiration=day,\
                    callput = callput, optionPrice=op_price)
                impliedVolatility = currentOption.impliedVolatility
                delta = currentOption.delta
                gamma = currentOption.gamma
                theta = currentOption.theta
                vega = currentOption.vega

            ivlist.append(impliedVolatility)
            deltalist.append(delta)
            gammalist.append(gamma)
            thetalist.append(theta)
            vegalist.append(vega)
            timelist.append(time)
            #print(row['month'],callput, eprice,impliedVolatility,delta,gamma,theta,vega)
            #print(impliedVolatility)
        df_all['delta']=deltalist 
        df_all['gamma']=gammalist 
        df_all['vega']=vegalist 
        df_all['theta']=thetalist 
        df_all['iv']=ivlist
        df_all['time']=timelist


        self.df_op = df_all.copy()
        #print (self.df_op)
        #self.df_op.to_csv('./Result1.csv',index=0) 
    
    

    def get_iv(self):
        '''
        50
        '''
        df_50 = self.df_op[self.df_op['name'].str.contains('50ETF购')]
        mindex = df_50['eprice'].drop_duplicates()
        eday = df_50['eday'].drop_duplicates()
        
        
        df_50call_res = pd.DataFrame(index = mindex,columns=eday)
        for date, row in df_50.T.iteritems():
            df_50call_res.loc[row['eprice'],row['eday']] = row['iv']
        df_50call_res['x'] =df_50call_res.index

        df_50_put = self.df_op[self.df_op['name'].str.contains('50ETF沽')]
        mindex = df_50_put['eprice'].drop_duplicates()
        eday = df_50_put['eday'].drop_duplicates()
        
        df_50put_res = pd.DataFrame(index = mindex,columns=eday)
        for date, row in df_50_put.T.iteritems():
            df_50put_res.loc[row['eprice'],row['eday']] = row['iv']
        df_50put_res['x'] =df_50put_res.index

        df_50res = pd.concat([df_50call_res,df_50put_res],axis=1)
        #df_50res['x'] =df_50res.index
        '''
        300
        '''
        df_300 = self.df_op[self.df_op['name'].str.contains('300ETF购')]
        mindex = df_300['eprice'].drop_duplicates()
        eday = df_300['eday'].drop_duplicates()
        
        df_300call_res = pd.DataFrame(index = mindex,columns=eday)
        for date, row in df_300.T.iteritems():
            df_300call_res.loc[row['eprice'],row['eday']] = row['iv']
        df_300call_res['x'] =df_300call_res.index

        df_300_put = self.df_op[self.df_op['name'].str.contains('300ETF沽')]
        mindex = df_300_put['eprice'].drop_duplicates()
        eday = df_300_put['eday'].drop_duplicates()
        
        df_300put_res = pd.DataFrame(index = mindex,columns=eday)
        for date, row in df_300_put.T.iteritems():
            df_300put_res.loc[row['eprice'],row['eday']] = row['iv']
        df_300put_res['x'] =df_300put_res.index

        df_300res = pd.concat([df_300call_res,df_300put_res],axis=1)
        
        return df_50res,df_300res
    
    def iv_month_50300(self):

        if self.df_op.empty:
            return
        df_50 = self.df_op[self.df_op['name'].str.contains('50ETF')]
        df_50 =df_50[df_50['iv']>0.1]
        months = df_50['eday'].drop_duplicates()
        meanlist =[]
        for month in months:
            iv_month = df_50[df_50['eday']==month]
            meanlist.append(iv_month.mean(axis=0)['iv'])
        df_res50 = pd.DataFrame()
        df_res50['date'] =months
        df_res50['iv'] =meanlist  
        df_res50.index = months

        df_300 = self.df_op[self.df_op['name'].str.contains('300ETF')]
        df_300 =df_300[df_300['iv']>0.1]
        months = df_300['eday'].drop_duplicates()
        meanlist =[]
        for month in months:
            iv_month = df_300[df_300['eday']==month]
            meanlist.append(iv_month.mean(axis=0)['iv'])
        df_res300 = pd.DataFrame()
        df_res300['date'] =months
        df_res300['iv'] =meanlist 
        df_res300.index = months   

        df_res = pd.concat([df_res50,df_res300],axis=1)
        #print(df_res) 
        return df_res

    def loop(self):
        while True:
            self.update_alldf()
            #self.iv_month_50300()
            time.sleep(RATE)

class HoldPositions:
    def __init__(self):
        #self.df = pd.DataFrame()
        print('yes')

    def update(self,data):
        greek =[0.0,0.0,0.0,0.0]
        try:
            df= pd.read_csv(r'./op.csv',usecols=[1,4,6],encoding='gbk')
        except:
            print('csv load faid')
        print(df)
        for d, row in df.T.iteritems(): 
            #print(row[0])
            code = 'CON_OP_'+str(row[0])
            longshort =1
            if row[1]=='卖':
                longshort =-1
            count = row[2]
            one_info = data[data['code']==code]
            #one_info.astype(float)
            #print(one_info['delta'].values,count,longshort)
            greek[0] += one_info['delta'].values*count*longshort
            greek[1] += one_info['gamma'].values*count*longshort
            greek[2] += one_info['vega'].values*count*longshort
            greek[3] += one_info['theta'].values*count*longshort
        #print(greek)
        return greek

if __name__ =='__main__':
    # df= pd.read_csv(r'./op.csv',usecols=[1,4,6],encoding='gbk')
    # print(df)

    model = DataModel()
    hp = HoldPositions()
    while True:
        if not model.df_op.empty:
            tmp = model.get_iv()
            print(tmp)
            hp.update(model.df_op)
        time.sleep(5)
    
    
    