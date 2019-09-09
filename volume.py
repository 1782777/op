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
        
        each_df.index =each_df.index.time
        if b==False:
            df_empty =each_df
            b=True

        df_empty = df_empty+each_df
        
mean_df = df_empty.div(df_empty.shape[0])
series = pd.Series(range(48), index=mean_df)
print (mean_df)

mean_df.plot()
plt.show()