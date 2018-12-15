import numpy as np
import pandas as pd 
import os
from setting import DATAPATH
from MatData import MatData
from Strategy import CalendarRebalance, ThresholdRebalance, available_select_method

# import MatData:
logret = MatData(pd.read_csv(os.path.join(DATAPATH,'mat_logret.csv')))
cap = MatData(pd.read_csv(os.path.join(DATAPATH,'mat_cap.csv')))
# in sample period: 2010/01 - 2016/12
# out of sample period: 2017/01 - 2017/12
logret_in = MatData(logret[:1761,:])
logret_out = MatData(logret[1762:,:])

# optimize calreb
for selectmethod in available_select_method:
    # loop through 3 select methods
    calreb = CalendarRebalance(n=10, select=selectmethod, weight='OptWeight')
    for steplength in range(20, 63, 5):
        for windowlength in range(252, 756, 63):
            calreb.setting(step=steplength, window=windowlength, 'ETQ', 0.0002)
            calreb.feed(logret=logret_in, cap=cap)
            calreb
# optimize thresreb
thresreb = ThresholdRebalance(n=10, select='TopCap', weight='OptWeight')