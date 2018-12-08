import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import os
from setting import DATAPATH
from MatData import MatData
from SelectMethod import TopCorr
from WeightMethod import CapWeight
from Process import PriceProcess

''' 
    based on:
        calendar rebalancing strategy,
        SelectMethod: TopCorr, 
        WeightMethod: CapWeight
'''

# instantiate MatData:
logret = MatData(pd.read_csv(os.path.join(DATAPATH,'mat_logret.csv')))
cap = MatData(pd.read_csv(os.path.join(DATAPATH,'mat_cap.csv')))
# ret = MatData(pd.read_csv(DATAPATH+'hist_pctchg.csv'))
# cap = MatData(pd.read_csv(DATAPATH+'mat_close.csv')) 
# logret = MatData(pd.read_csv(DATAPATH+'mat_ret.csv'))

# step1: specify size N
N = 10


# step2: loop through sample period
# implement selecting and weighting method
# ex.calendar rebalancing
DELTA = 30
WINDOW = 30
# begin after WINDOW
# end before T - DELTA
port_prc_proc = PriceProcess()
index_prc_proc = PriceProcess()
for i in range(WINDOW, len(logret)-DELTA, DELTA):

    # decision period
    dec_cap = cap[i-1:i, 1:]
    dec_logret = logret[i-WINDOW:i,:]
    topcorr = TopCorr(dec_logret)
    sel_ticker = topcorr.select(n=10)
    capweight = CapWeight(dec_cap[sel_ticker])
    sel_shares = capweight.weight()

    # holding period
    hold_index_ret = logret[i:i+DELTA, 0]
    temp_index_prc_proc = (
        np.exp(hold_index_ret.cumsum())
    )
    index_prc_proc.append(temp_index_prc_proc)

    hold_port_ret = logret[i:i+DELTA][sel_ticker]
    temp_port_prc_proc = (
        sel_shares.values * np.exp(hold_port_ret.cumsum())
    ).agg('sum', axis=1)
    port_prc_proc.append(temp_port_prc_proc)
    


    
port_prc_proc.plotvs(index_prc_proc)

# evalutate out-of-sample period



