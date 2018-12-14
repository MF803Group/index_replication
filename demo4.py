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
from TrkErrMeasure import ETQ
''' 
    based on:
        threshold rebalancing strategy,
        SelectMethod: TopCap / TopCorr / PCA
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

WINDOW = 360
THRESHOLD = 0.02
# begin after WINDOW
port_wgt_proc = WeightProcess()
port_prc_proc = PriceProcess()
index_prc_proc = PriceProcess()

i = WINDOW

while(i < len(logret)):
    date = logret.index[i]
    print(date)
    # -----  decision period ----- #
    # select

    dec_logret = logret[i-WINDOW:i,:]
    dec_index_logret = logret[i-WINDOW:i,0]

    dec_cap = cap[i-WINDOW:i, 1:]
    topcap = TopCap(dec_cap, N)
    sel_ticker = topcap.select()

    # pca = PCA(dec_logret)
    # sel_ticker = pca.select(n=N)

    # topcorr = TopCorr(dec_logret)
    # sel_ticker = topcorr.select(n=N)
    
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
    
    temp_index_prc_proc = PriceProcess()
    temp_port_prc_proc = PriceProcess()
    trk_err = 0.0
    while(trk_err <= THRESHOLD and i < len(logret)):

        # ----- holding period ----- #
        step_index_ret = logret[i:i+1, 0]
        temp_index_prc_proc.append(np.exp(step_index_ret))

        step_port_ret = logret[i:i+1][sel_ticker]
        temp_port_prc_proc.append((
            sel_weight * np.exp(step_port_ret)
        ).agg('sum', axis=1))

        trk_err = ETQ(temp_index_prc_proc.s, temp_port_prc_proc.s)
        print(trk_err)
        i += 1
    
    index_prc_proc.append(temp_index_prc_proc.s)
    port_prc_proc.append(temp_port_prc_proc.s)

    


    
port_prc_proc.plotvs(index_prc_proc)

# evalutate out-of-sample period



