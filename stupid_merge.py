import pandas as pd
import numpy as np

df1 = pd.DataFrame(np.random.randn(525600,4), 
                   index=pd.date_range('1/1/2011', 
                   periods=525600, freq='Min'), 
                   columns=list('ABCD'))

df2 = pd.DataFrame(np.random.randn(8760,4), 
                   index=pd.date_range('1/1/2011',
                   periods=8760,
                   freq='H'), 
                   columns=list('ZYXW'))

merged = pd.merge(df1,df2,
                  left_on=[df1.index.year, df1.index.month, df1.index.day, df1.index.hour], 
                  right_on=[df2.index.year, df2.index.month, df2.index.day, df2.index.hour])

# .drop(['key_0','key_1','key_2','key_3'], axis = 1)

