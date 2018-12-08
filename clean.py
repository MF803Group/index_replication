import numpy as np
import pandas as pd 
import os
from setting import DATAPATH
from MatData import MatData

''' 
    this code sets data of ticker(not in hist_s&p_const) to nan
'''

mat_component = pd.read_csv(os.path.join(DATAPATH,"hist_s&p_const.csv"))
mat_component = mat_component.transpose()
mat_component.index = pd.to_datetime(mat_component.index)

mat_logret = pd.read_csv(os.path.join(DATAPATH,"hist_logret.csv"))
mat_logret = MatData.index_setting(mat_logret)

mat_cap = pd.read_csv(os.path.join(DATAPATH,"hist_cap.csv"))
mat_cap = MatData.index_setting(mat_cap)


print(mat_component.shape, mat_logret.shape, mat_cap.shape)
i = 0
j = 0
while(i < len(mat_component) and j < len(mat_logret)) :
    if mat_component.index[i] <= mat_logret.index[j] and \
        mat_component.index[i+1] >= mat_logret.index[j] :
        
        valid_list = list(mat_component.iloc[i,:].dropna().values)
        now_list = list(mat_logret.iloc[j,1:].index)

        invalid_list = list(set(now_list) - set(valid_list))

        mat_logret.iloc[j,1:][invalid_list] = np.nan
        mat_cap.iloc[j,:][invalid_list] = np.nan

        j += 1
        continue
    else:  
        i += 1
        continue

mat_logret.to_csv(os.path.join(DATAPATH,"mat_logret.csv"))
mat_cap.to_csv(os.path.join(DATAPATH,"mat_cap.csv"))

