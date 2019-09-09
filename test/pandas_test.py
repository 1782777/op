import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

df= pd.read_excel('test/000016_5_l.xlsx',usecols=[0, 16],skipfooter=1,skiprows=[0,1,3],parse_dates=['      时间'],index_col='      时间')



pd_index=df.index.to_period("D")
dup_data = pd_index.drop_duplicates(keep='first')


df_empty = pd.DataFrame()
b = False

for i in dup_data:
    each_df = df[str(i)]
    if each_df.shape[0]==48:
        # series = pd.Series(range(48), index=each_df.index)
        # series.resample('60S').bfill()[0:5]
        # print(series)
        each_df.index =each_df.index.time
        if b==False:
            df_empty =each_df
            b=True

        df_empty = df_empty+each_df
        
mean_df = df_empty.div(df_empty.shape[0])
series = pd.Series(range(48), index=mean_df)

# series.resample('30S').bfill()[0:5]
print (mean_df)

mean_df.plot()
plt.show()
#date = df.loc['20170823']
#print(date)

# day = df['      时间'].dt.date
# print(day)  
# df_dt=pd.to_datetime(df['      时间'])

# df2 = df.set_index('      时间')
# print(df_dt)

# print (df['      时间'])
# df_dt=pd.to_datetime(df['      时间'])
# print(df_dt)

#s_d=df_dt.dt.day
# df_dt=pd.to_datetime(df['时间'],format="%Y/%m/%d")
# print (df_dt)
