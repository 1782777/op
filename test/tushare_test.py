import tushare as ts
import matplotlib.pyplot as plt
import numpy as np

data =ts.get_hist_data('000016', ktype='5')
# x = data.index
# y=data['volume']

# plt.plot(x ,y,color ='red', linewidth=2.5) 
# plt.show()

# for i in data.index:
#     d =data.loc[:,'volume']
#     print(d)

#print(data['2019-08-21 09:05:00':'2019-08-24' '09:05:00'])

# a =data.iloc[1:2]
time =data.index
#count =time.shape[0]
indexs = []
for d in time:
    indexs.append(d.split(' ')[0])
    

np_date = np.array(indexs)
np_date = np.unique(np_date)
#print(np_date)

for i in range(0,np_date.shape[0]-1):
    #print (np_date[i])
    oneday = data[np_date[i+1]:np_date[i]]
    print (oneday.shape)

#print(row)
#print(time.split(' ')[0])
#print(data['2019-08-23':'2019-08-22'])


