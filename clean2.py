import numpy as np
import pandas as pd 
import os
from setting import DATAPATH
from MatData import MatData

#TODO: unfinished！！！ require goog & googl data
''' 
    this code solves class a, b, and c problem
'''

mat_cap = pd.read_csv(os.path.join(DATAPATH,"hist_cap.csv"))
mat_cap = MatData.index_setting(mat_cap)

mat_logret = pd.read_csv(os.path.join(DATAPATH,"hist_logret.csv"))
mat_logret = MatData.index_setting(mat_logret)

print(mat_logret.shape, mat_cap.shape)

i = 0
while(i < len(mat_logret)):
    pass     
