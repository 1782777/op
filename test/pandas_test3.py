from pandas import Series,DataFrame
import pandas as pd
import numpy as np
from numpy import nan#导入相应模块
import matplotlib.pyplot as plt
#插入数据
df1 = DataFrame(np.arange(12).reshape((3,4)),columns=list("abcd"))
df2 = DataFrame(np.arange(20).reshape((4,5)),columns=list("abcde"))
df1
df2
df3 =df1+df2#df1.add(df2)
df3.iloc[1, 3] =nan
df1.add(df2,fill_value=0)# 为df1添加第3行和e这一列，并将其填充为0
df1.add(df2).fillna(0)# 按照正常方式将df1和df2相加，然后将NaN值填充为0
print(df3)
df3.plot()
plt.show()