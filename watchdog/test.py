# import matplotlib.pyplot as plt
# fig, ax = plt.subplots()
# y1 = []
# for i in range(50):
#     y1.append(i)  # 每迭代一次，将i放入y1中画出来
#     ax.cla()
#     for j in range(10000000):
#         a =j+1
#     ax.bar(y1, label='test', height=y1, width=0.3)
#     #ax.legend("1111")
#     plt.pause(0.4)


# import matplotlib.pyplot as plt
# import numpy as np
 
# x = np.arange(0,10,0.1)
 
# y1 = 0.05 * x**2
# y2 = -1 * y1
 
# fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()
# ax1.plot(x,y1,'g-')
# ax2.plot(x,y2,'b-')
 
# ax1.set_xlabel("X data")
# ax1.set_ylabel("Y1",color='g')
 
# ax2.set_ylabel("Y2",color='b')
 
# plt.show()


from requests import get
import json
import pandas as pd
import matplotlib.pyplot as plt

# url ='http://img1.money.126.net/data/hs/time/today/0000016.json'
# datas = get(url).json()['data']['yestclose']
# pf = pd.DataFrame(datas,columns=['time','current','no','volume'])
# last_price = get(url).json()['yestclose']

# print (pf,last_price)


# url ='http://push2.eastmoney.com/api/qt/kamt.rtmin/get?fields1=f1&fields2=f51,f52,f54,f56&ut=b2884a393a59ad64002292a3e90d46a5'
# datas = get(url).json()['data']['s2n']
# all=[]
# for data in datas:
#     line = data.split(',')
#     all.append(line)
# #dic= dict(all)
# print (all)
# pf = pd.DataFrame(all,columns=['time','sgt','hgt','all'])
# print (pf)


url ='http://1.optbbs.com/d/csv/d/data.csv'
datas = get(url).text
df = pd.read_csv(url)
pd.to_datetime(df['Time'])
df.index = df['Time']
print(df.columns)
df = df.drop(['Time','Pre','max','min'],axis=1)
df.plot()
plt.show()

print(df)

# all =[]
# lines = datas.split('\n')
# for line in lines:
#     texts = line.split(',')
#     all.append(texts)

# df = pd.DataFrame(all,columns=['time','iv','pre','max','min'])
# print (df)
# all=[]
# for data in datas:
#     line = data.split(',')
#     all.append(line)
# #dic= dict(all)
# print (all)
# pf = pd.DataFrame(all,columns=['time','sgt','hgt','all'])
# print (pf)
