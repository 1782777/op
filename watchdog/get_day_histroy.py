import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt


class history:
    def __init__(self):
        self.df= pd.read_excel('./000016.xlsx',usecols=[0, 16],skipfooter=1,skiprows=[0,1,3],parse_dates=['      时间'],index_col='      时间')
        pd_index=self.df.index.to_period("D")
        self.dup_data = pd_index.drop_duplicates(keep='first')
        #print(self.df)

    def get_dayMean(self):
        b = False
        df_empty = pd.DataFrame()
        count_day =0
        for i in self.dup_data:
            
            each_df = self.df[str(i)]
            #print(each_df)
            if each_df.shape[0]==240:
                count_day = count_day+1
                each_df.index =each_df.index.time
                if b==False:
                    df_empty =each_df
                    b=True
                else:
                    df_empty = df_empty+each_df
        #print(df_empty.shape[0])        
        #mean_df = df_empty.div(df_empty.shape[0])
        mean_df = df_empty.cumsum()
        
        mean_df = mean_df/count_day

        
        #series = pd.Series(range(240), index=mean_df)
        
        return mean_df

if __name__ == '__main__':
    his = history()
    mean_df=his.get_dayMean()
    #print(mean_df)
    mean_df.plot()
    plt.show()



