import pandas as pd 
import numpy as np 

df= pd.read_excel('test/000016_5_l.xlsx',usecols=[0, 16],skipfooter=1,skiprows=[0,1,3],parse_dates=['      时间'],index_col='      时间')

print(df)
# df_dt=pd.to_datetime(df['      时间'])

# df2 = df.set_index('      时间')
# print(df_dt)

# print (df['      时间'])
# df_dt=pd.to_datetime(df['      时间'])
# print(df_dt)

#s_d=df_dt.dt.day
# df_dt=pd.to_datetime(df['时间'],format="%Y/%m/%d")
# print (df_dt)
