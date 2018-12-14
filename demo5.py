import numpy as np
import pandas as pd 
import os
from setting import DATAPATH
from MatData import MatData
from Strategy import CalendarRebalance, ThresholdRebalance

# import MatData:
logret = MatData(pd.read_csv(os.path.join(DATAPATH,'mat_logret.csv')))
cap = MatData(pd.read_csv(os.path.join(DATAPATH,'mat_cap.csv')))

# choose size n
# select method: TopCap / TopCorr / PCA
# weight method: CapWeight / OptWeight
# strategy: CalendarRebalance / ThresholdRebalance
calreb = CalendarRebalance(n=10, select='TopCap', weight='OptWeight')

# specify step length (defalut:30)
# specify decision window length (defalut:360)
# specify transaction cost ratio 
calreb.setting(step=60, window=360, trans_ratio=0.0)

# feed data to strategy
calreb.feed(logret=logret, cap=cap)

# run strategy
calreb.run()

# TODO:evalutate
calreb.port_prc_proc.plotvs(calreb.index_prc_proc)




