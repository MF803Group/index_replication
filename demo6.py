import numpy as np
import pandas as pd 
import os
from setting import DATAPATH
from MatData import MatData
from Strategy import ThresholdRebalance

# import MatData:
logret = MatData(pd.read_csv(os.path.join(DATAPATH,'mat_logret.csv')))
cap = MatData(pd.read_csv(os.path.join(DATAPATH,'mat_cap.csv')))

# choose size n
# select method: TopCap / TopCorr / PCA
# weight method: CapWeight / OptWeight
# strategy: ThresholdRebalance
thresreb = ThresholdRebalance(n=10, select='TopCap', weight='OptWeight')

# specify step length (defalut:30)
# specify decision window length (defalut:360)
# specify measure kind (defalut:ETQ)
# specify transaction cost ratio (defalut:0.0)
thresreb.setting(window=360, measure_kind='MAD', threshold=0.02, trans_ratio=0.0)

# feed data to strategy
thresreb.feed(logret=logret, cap=cap)

# run strategy
thresreb.run(printer=True)

# TODO:evalutate
thresreb.port_prc_proc.plotvs(thresreb.index_prc_proc)




