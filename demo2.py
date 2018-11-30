import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from setting import DATAPATH
from MatData import MatData
from SelectMethod import TopCap
from WeightMethod import CapWeight
from PriceProcess import PriceProcess

# instantiate MatData:
cap = MatData(pd.read_csv(DATAPATH+'hist_cap.csv')) 
ret = MatData(pd.read_csv(DATAPATH+'hist_pctchg.csv'))
ret.df = ret.df / 100 

# step1: specify size N
N = 5


# step2: loop through sample period
# implement selecting and weighting method
# ex.calendar rebalancing
DELTA = 30
WINDOW = 1
# begin after WINDOW
# end before T - DELTA
port_prc_proc = PriceProcess()
index_prc_proc = PriceProcess()
for i in range(WINDOW, len(ret)-DELTA, DELTA):

    # decision period
    dec_cap = cap[i-WINDOW:i, 1:]
    topcap = TopCap(dec_cap, N)
    sel_ticker = topcap.select()
    capweight = CapWeight(dec_cap[sel_ticker])
    sel_shares = capweight.weight()

    # holding period
    hold_port_ret = ret[i:i+DELTA][sel_ticker]
    temp_port_prc_proc = (
        sel_shares.values * np.exp(hold_port_ret.cumsum())
    ).agg('sum', axis=1)
    port_prc_proc = port_prc_proc.append(temp_port_prc_proc)

    hold_index_ret = ret[i:i+DELTA, 0]
    temp_index_prc_proc = (
        np.exp(hold_index_ret.cumsum())
    )
    index_prc_proc = index_prc_proc.append(temp_index_prc_proc)
    
port_prc_proc.plot(index_prc_proc)

# evalutate out-of-sample period



