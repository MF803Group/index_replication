import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from setting import DATAPATH
from MatData import MatData
from SelectMethod import TopCap
from WeightMethod import CapWeight

# instantiate MatData:
close = MatData(pd.read_csv(DATAPATH+'mat_close.csv')) 
ret = MatData(pd.read_csv(DATAPATH+'mat_ret.csv')) 


# step1: specify size N
N = 2


# step2: loop through sample period
# implement selecting and weighting method
# ex.calendar rebalancing
DELTA = 30
WINDOW = 1
# begin after WINDOW
# end before T - DELTA
for i in range(WINDOW, len(ret)-DELTA, DELTA):

    # decision period
    dec_close = close[i-WINDOW:i, 1:]
    topcap = TopCap(dec_close, N)
    sel_ticker = topcap.select()
    capweight = CapWeight(dec_close[sel_ticker])
    sel_shares = capweight.weight()

    # holding period
    hold_port_ret = ret[i:i+DELTA][sel_ticker]
    port_prc_proc = (
        sel_shares.values * np.exp(hold_port_ret.cumsum())).agg(
            'sum', axis=1
        )
    hold_index_ret = ret[i:i+DELTA, 0]
    index_prc_proc = np.exp(hold_index_ret.cumsum())
    
    plt.figure()
    port_prc_proc.name = 'tracking portfolio'
    port_prc_proc.plot()
    index_prc_proc.name = 'index'
    index_prc_proc.plot()
    plt.legend()
    plt.show()

    break

# evalutate out-of-sample period



