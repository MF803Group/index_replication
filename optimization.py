import numpy as np
import pandas as pd 
import os
from setting import DATAPATH, RESULTPATH
from MatData import MatData
from Strategy import CalendarRebalance, ThresholdRebalance, available_select_method

step_range = range(20, 63, 5)
window_range = range(252, 756, 63)

trivial_step_range = range(20, 21, 5)
trivial_window_range = range(252, 253, 63)

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
    calreb = CalendarRebalance(n=10, select=selectmethod, weight='OptWeight')
    for steplength in step_range:
        for windowlength in window_range:
            print(selectmethod, steplength, windowlength)
            calreb.setting(step=steplength, window=windowlength, measure_kind='ETQ', trans_ratio=0.0002)
            calreb.feed(logret=logret_in, cap=cap_in)
            calreb.run(printer=False)
            trk_err = calreb.evalute(printer=False)
            string = "_".join([str(selectmethod), str(steplength), str(windowlength)])
            res[string] = trk_err
res_df = pd.Series(res)
res_df.to_csv(os.path.join(RESULTPATH,'calreb_optimize.csv'))
# optimize thresreb
# thresreb = ThresholdRebalance(n=10, select='TopCap', weight='OptWeight')