import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import os
from setting import DATAPATH
from MatData import MatData
from SelectMethod import PCA, TopCap, TopCorr
from WeightMethod import OptWeight
from Process import PriceProcess
from MultiProcess import WeightProcess

''' 
    based on:
        calendar rebalancing strategy,
        SelectMethod: TopCap, 
        WeightMethod: OptWeight
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
WINDOW = 360
# begin after WINDOW
# end before T - DELTA
port_wgt_proc = WeightProcess()
port_prc_proc = PriceProcess()
index_prc_proc = PriceProcess()

for i in range(WINDOW, len(logret)-DELTA, DELTA):

    date = logret.index[i]
    print(date)
    # -----  decision period ----- #
    # select
    dec_logret = logret[i-WINDOW:i,:]
    dec_index_logret = logret[i-WINDOW:i,0]

    # dec_cap = cap[i-WINDOW:i, 1:]
    # topcap = TopCap(dec_cap, N)
    # sel_ticker = topcap.select()

    # pca = PCA(dec_logret)
    # sel_ticker = pca.select(n=N)

    topcorr = TopCorr(dec_logret)
    sel_ticker = topcorr.select(n=N)
    
    print(sel_ticker)
    dec_pool_logret = dec_logret[sel_ticker]
    # weight
    optweight = OptWeight(
        dec_pool_logret, 
        dec_index_logret, 
        port_wgt_proc
    )
    sel_weight = optweight.weight()

    temp_port_wgt_proc = WeightProcess(date, sel_ticker, sel_weight)
    port_wgt_proc.append(temp_port_wgt_proc)
    
    # ----- holding period ----- #
    hold_index_ret = logret[i:i+DELTA, 0]
    temp_index_prc_proc = (
        np.exp(hold_index_ret.cumsum())
    )
    index_prc_proc.append(temp_index_prc_proc)

    hold_port_ret = logret[i:i+DELTA][sel_ticker]
    temp_port_prc_proc = (
        sel_weight * np.exp(hold_port_ret.cumsum())
    ).agg('sum', axis=1)
    port_prc_proc.append(temp_port_prc_proc)
    


    
port_prc_proc.plotvs(index_prc_proc)

# evalutate out-of-sample period



