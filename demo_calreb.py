import numpy as np
import pandas as pd 
import os
from setting import DATAPATH
from MatData import MatData
from Strategy import CalendarRebalance

# import MatData:
logret = MatData(pd.read_csv(os.path.join(DATAPATH,'mat_logret.csv')))
cap = MatData(pd.read_csv(os.path.join(DATAPATH,'mat_cap.csv')))

# choose size n
# select method: TopCap / TopCorr / PCA
# weight method: CapWeight / OptWeight
calreb = CalendarRebalance(n=10, select='TopCorr', weight='OptWeight')

# specify step length (defalut:30)
# specify decision window length (defalut:360)
# specify measure kind (defalut:ETQ)
# specify transaction cost ratio (defalut:0.0)
calreb.setting(step=60, window=360, measure_kind='ETQ', trans_ratio=0.005)

# feed data to strategy
calreb.feed(logret=logret, cap=cap)

# run strategy
calreb.run(printer=True)

# TODO:evalutate
calreb.evalute()



