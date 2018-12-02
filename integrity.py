import pandas as pd 
import os
from setting import DATAPATH


mat_logret = pd.read_csv(os.path.join(DATAPATH,"hist_logret.csv"))
mat_component = pd.read_csv(os.path.join(DATAPATH,"hist_s&p_const.csv"))
print(mat_logret.shape, mat_component.shape)
for i in range(mat_logret.shape[0]):
    print()
    print()
    # print(mat_logret.iloc[i,:].isna().sum())

