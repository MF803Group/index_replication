import numpy as np
import pandas as pd 
import os
from setting import DATAPATH, RESULTPATH
from MatData import MatData
from Strategy import ThresholdRebalance, available_select_method

window_range = range(252, 756, 63)
threshold_range = np.arange(0.01, 0.03, 0.004)

# import MatData:
logret = MatData(pd.read_csv(os.path.join(DATAPATH,'mat_logret.csv')))
cap = MatData(pd.read_csv(os.path.join(DATAPATH,'mat_cap.csv')))
# in sample period: 2010/01 - 2016/12
# out of sample period: 2017/01 - 2017/12
logret_in = MatData(logret[:1761,:])
cap_in = MatData(cap[:1761,:])
logret_out = MatData(logret[1762:,:])

# optimize calreb
res = dict()
for selectmethod in available_select_method:
    # loop through 3 select methods
    thresreb = ThresholdRebalance(n=10, select=selectmethod, weight='OptWeight')
    for windowlength in window_range:
        for thresholdlength in threshold_range:
            print(selectmethod, windowlength, thresholdlength)
            thresreb.setting(window=windowlength, measure_kind='ETQ', threshold=thresholdlength ,trans_ratio=0.0002)
            thresreb.feed(logret=logret_in, cap=cap_in)
            thresreb.run(printer=False)
            trk_err = thresreb.evalute(printer=False)
            string = "_".join([str(selectmethod), str(windowlength), str(thresholdlength)])
            res[string] = trk_err
res_df = pd.Series(res)
res_df.to_csv(os.path.join(RESULTPATH,'calreb_optimize.csv'))
