# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 08:15:50 2018

@author: Brian
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def DateFmtInt(dateA):
    dateA = str(dateA)
    dateA = dateA.replace(' ','')
    dateA = dateA.replace('-','')
    dateA = int(dateA)
    return dateA
def MTimeSerPlot(df, title, xlabel, col_lst=["grey", "black"], lgd_loc="upper left"):
    df.index = [str(x) for x in df.index]
    dat_lst = list(df.index)
    fd_lst = list(df.columns)
    fd_cnt = len(fd_lst)
    fig = plt.figure()
    fig1 = fig.add_subplot(1,1,1)
    for n in range(fd_cnt):
        cr = col_lst[n%len(col_lst)]
        fd = fd_lst[n]
        fig1.plot(dat_lst, df[fd], color=cr, label=fd)
    plt.legend(loc="upper left")
    fig1.set_title(title)
    fig1.set_xlabel(xlabel)
    fig1.set_xticks([])
    plt.show()


### Main Tracking error function:
def TrkErr(stk_ret, wgt, cost_ratio, start_date, end_date):
    ### Stock returns and weights
    path_now = os.path.abspath('.') # this line will be deleted
    path_ret = path_now + "\Input\Ret" # this line will be deleted
    stk_ret = pd.read_csv(path_ret+"\mat_ret.csv") # this line will be deleted
    stk_ret = stk_ret.set_index("Date")
    stk_ret.index = [DateFmtInt(x) for x in stk_ret.index]
    stk_ret = stk_ret[stk_ret.index>=start_date]
    stk_ret = stk_ret[stk_ret.index<=end_date]
    dat_lst = list(stk_ret.index)
    dat_cnt = len(dat_lst)
    cmp_df = pd.DataFrame()
    cmp_df["IND Ret"] = stk_ret["SP500"]
    cmp_df["REP Ret"] = np.zeros((dat_cnt,1))
    cmp_df["IND NAV"] = np.ones((dat_cnt,1))
    cmp_df["REP NAV"] = np.ones((dat_cnt,1))
    stk_ret = stk_ret.drop("SP500", axis=1)
    stk_nam_lst = list(stk_ret.columns)
    stk_cnt = len(stk_nam_lst)
    wgt = pd.DataFrame(np.random.normal(0.2,0.2,(dat_cnt, stk_cnt)), columns=stk_nam_lst, index=dat_lst) # this line will be deleted
    wgt.iloc[0:(round(dat_cnt*1/3)),:] = [0.2,0.8,0.0,0.0,0.0] # this line will be deleted
    wgt.iloc[(round(dat_cnt*1/3)):(round(dat_cnt*2/3)),:] = [0.2,0.5,0.1,0.1,0.1] # this line will be deleted
    wgt.iloc[(round(dat_cnt*2/3)):,:] = [0.2,0.2,0.2,0.2,0.2] # this line will be deleted
    print("Parameter Settings:")
    print("Start date:", dat_lst[0])
    print("End date:", dat_lst[-1])
    print("Ratio of transaction costs:", cost_ratio*100, "%")
    for rw in range(dat_cnt):
        cmp_df["REP Ret"][dat_lst[rw]] = np.matrix(stk_ret.iloc[[rw]]*wgt.iloc[[rw]]).sum()
        if rw>=1:
            u1 = np.matrix(wgt.iloc[[rw]]) - np.matrix(wgt.iloc[[rw-1]])
            u2 = abs(u1).sum()
            cmp_df["REP Ret"][dat_lst[rw]] -= u2*cost_ratio
            if u2>0:
                print("Date", dat_lst[rw], "total rebalancing weight:", u2)
            cmp_df["IND NAV"][dat_lst[rw]] = cmp_df["IND NAV"][dat_lst[rw-1]] * (1+cmp_df["IND Ret"][dat_lst[rw]])
            cmp_df["REP NAV"][dat_lst[rw]] = cmp_df["REP NAV"][dat_lst[rw-1]] * (1+cmp_df["REP Ret"][dat_lst[rw]])
    u1 = cmp_df.loc[:,["IND NAV", "REP NAV"]]
    MTimeSerPlot(u1, title="Replicated portfolio VS S&P500 Index", xlabel=(str(start_date)[0:6]+" ~ "+str(end_date)[0:6]))
    ETQ = 0
    MSE = 0
    MXE = 0
    dat_lst = list(cmp_df.index)
    for rw in range(len(dat_lst)):
        ETQ += abs(cmp_df["REP NAV"][dat_lst[rw]] - cmp_df["IND NAV"][dat_lst[rw]])
        MSE += (cmp_df["IND Ret"][dat_lst[rw]] - cmp_df["REP Ret"][dat_lst[rw]])**2
        cmd = abs(cmp_df["REP NAV"][dat_lst[rw]]/cmp_df["IND NAV"][dat_lst[rw]]-1)
        MXE=cmd if MXE<cmd else MXE
    ETQ/= len(dat_lst)
    MSE/= len(dat_lst)
    print("Ex. post tracking quality (ETQ):", round(ETQ*100,3), "%")
    print("MeanSquaredError of returns:", round(MSE*100,3), "%")
    print("Max. cumulative tracking difference:", round(MXE*100,3), "%")    

    
### Parameter Setting
start_date = 20171100
end_date = 20181099
cost_ratio = 0.05/100*1000


TrkErr("", "", cost_ratio, start_date, end_date)










