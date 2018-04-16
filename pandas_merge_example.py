#%% import libs
import pandas as pd
import numpy as np

#%% make fake dataframes with datetimeindex
# df1 is has minute intervals
# df2 has hour intervals
df1 = pd.DataFrame(np.random.randn(525600,4), 
                   index=pd.date_range('1/1/2011', 
                   periods=525600, freq='Min'), 
                   columns=list('ABCD'))

df2 = pd.DataFrame(np.random.randn(8760,4), 
                   index=pd.date_range('1/1/2011',
                   periods=8760,
                   freq='H'), 
                   columns=list('ZYXW'))

#%% Works but is hella ugly
df1['Year'] = df1.index.year
df1['Month'] = df1.index.month
df1['Day'] = df1.index.day
df1['Hour'] = df1.index.hour
df2['Year'] = df2.index.year
df2['Month'] = df2.index.month
df2['Day'] = df2.index.day
df2['Hour'] = df2.index.hour
ymdh = ['Year','Month','Day','Hour']
merged = pd.merge(df1,df2,on=ymdh,how='left').drop(ymdh,axis=1)
merged.index = df1.index

#%% Works but is hella slow
df1['per'] = df1.index.to_period('H')
df2['per'] = df2.index.to_period('H')
merged = pd.merge(df1,df2,how='left',on='per').drop('per',axis=1)
merged.index = df1.index

#%% Key Error
merged = pd.merge(df1,df2,
                  left_on=[df1.index.year, df1.index.month, df1.index.day, df1.index.hour], 
                  right_on=[df2.index.year, df2.index.month, df2.index.day, df2.index.hour]
                  ).drop(['key_0','key_1','key_2','key_3'], axis = 1)
merged.index = df1.index

#%% Key Error
merged = pd.merge(df1, df2, how='left', left_on = df1.index.to_period('H'), right_on = df2.index.to_period('H'))
merged.index = df1.index

#%% Sort Error
merged = pd.merge(df1.set_index(df1.index.to_period('H')), 
             df2.set_index(df2.index.to_period('H')), 
             how = 'left',left_index=True,right_index=True)
merged.index = df1.index
