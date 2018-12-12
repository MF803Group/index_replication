# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 08:15:50 2018

@author: Brian
"""



import pandas as pd
import numpy as np
import scipy.optimize as opt
import datetime
from math import e
import time
import matplotlib.pyplot as plt
from setting import DATAPATH



from sklearn.decomposition import PCA as pca



# Setting dataframe displayed rows
pd.set_option('display.max_rows', 12)



def Pca(stk_ret):  
    df = stk_ret.copy()
    # drop stocks that are not listed, and save stock index in a dict
    df = df.dropna(axis=1,how='any')
    ticker_name = df.columns
    ticker_dict = {x: y for x, y in enumerate(ticker_name)}
            
    # construct the pca model and fit the model with data
    sample = df.values
    model = pca(n_components=n_components)
    model.fit(sample)
        
    # compute PCA components and corresponding variance ratio
    pcs = model.components_
    pcs_mat = np.matrix(pcs)
    var_ratio = model.explained_variance_ratio_
    var_ratio_mat = np.matrix(var_ratio)
        
    # compute overall loadings for each stock
    load_mat = var_ratio_mat*pcs_mat
        
    # find top 20 stocks with largest loadings
    load_arr = np.asarray(load_mat).reshape(-1)
    load_dict = {y: x for x, y in enumerate(load_arr)}
    sort_load = sorted(load_arr, key=abs, reverse=True)
    top_load = sort_load[:n]
    ticker_num = [load_dict[x] for x in top_load]
    selected_ticker = [ticker_dict[x] for x in ticker_num]
    all_tc = ["S&P"]
    all_tc.extend(selected_ticker)
    return all_tc



def PrpRet(stk_ret0, opr):
    ### Preparation of stock returns data
    stk_ret = stk_ret0.copy()
    stk_ret = stk_ret.set_index("Date")
    stk_ret.index = [int(x) for x in stk_ret.index]
    ss = rdt(start_date, "%Y/%m/%d")
    ee = rdt(end_date, "%Y/%m/%d")
    si = ds(ss,1)
    ei = ds(ee,1)
    if opr==1:
        stk_ret = stk_ret[stk_ret.index>=si]
        stk_ret = stk_ret[stk_ret.index<ei]
    else:
        stk_ret = stk_ret[stk_ret.index>=sss] 
        stk_ret = stk_ret[stk_ret.index<eee]
    stk_ret = e**stk_ret-1
    stk_ret = stk_ret.fillna(0)
    return stk_ret, ss, ee, si, ei
    
    
    
def GnrW(wgt_lst, rbl_lst, dat_lst, stk_nam_lst):
    wgt = pd.DataFrame(columns=stk_nam_lst)
    wgt["Date"] = pd.Series(dat_lst)
    wgt = wgt.set_index("Date")
    ss = rdt(start_date, "%Y/%m/%d")
    ee = rdt(end_date, "%Y/%m/%d")
    si = ds(ss,1)
    ei = ds(ee,1)
    wgt = wgt[wgt.index>=si]
    wgt = wgt[wgt.index<ei]
    dat_cnt = len(wgt.index)
    rbl_lst2 = rbl_lst
    rbl_lst2.append(99999999)
    rw = 0
    ind = 0
    while rw<=(dat_cnt-1):
        if wgt.index[rw]>=rbl_lst2[ind] and wgt.index[rw]<rbl_lst2[ind+1]:
            wgt.iloc[rw] = wgt_lst[ind]
            rw += 1        
        else:
            ind += 1
            continue
    return wgt
        
        
        
def GnrDate(start_date, end_date, rbl_wnd, bck_wnd): 
    """ 
        Generating backtesting time interval and reblance dates
        Input: start_date, end_date, reblance window, backtesting window
        Display: /
        Output: list of rebalancing dates, list of backtesting date pairs, 
                number of rebalancing times
    """
    rbl_wnd = round(rbl_wnd*365.25, 0)
    bck_wnd = round(bck_wnd*365.25, 0)
    ss = rdt(start_date, "%Y/%m/%d")
    ee = rdt(end_date, "%Y/%m/%d")
    ei = ds(ee,1)
    rbl_lst = []
    bck_lst = []
    cr = ss
    while ds(cr,1)<=ei:
        qn = ds(cr,1)
        ql = ds(cr,1,-bck_wnd)
        rbl_lst.append(qn)
        bck_lst.append([ql,qn])
        cr = ds(cr,0,rbl_wnd)
    nrb = len(rbl_lst)
    return rbl_lst, bck_lst, nrb

def rdt(strA, FMT):
    """ 
        Generating datetime.strptime date from str
    """
    return datetime.datetime.strptime(str(strA), FMT)

def ds(datetimeA, fmt=0, sft=0):
    """ 
        Shifting datetime.strptime date (and change it into integer)
    """
    d1 = datetime.timedelta(sft)
    datetimeA += d1
    dateA = int(str(datetimeA)[:10].replace('/','').replace('-',''))
    return (dateA if (fmt==1) else datetimeA)



def LstFndInd(lst, tck):
    try:
        lst.index(tck)
        return lst.index(tck)
    except:
        return -1
    
    

def MTimeSerPlot(df, title, xlabel, col_lst=["grey", "black"], lgd_loc="upper left"):
    """ 
        Ploting multiple time series
        Input: dataframe consisting several time series,
               figure title, xlabel name, list of colors, location of legends
        Display: plot
        Output: /
    """
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



### Single/Whole period tracking error:
def TrkErr(W, opr=0, err_type="ETQ"):
    """ 
        Calculating tracking errors
        Input: dataframe of weights of stocks, operation (0: back-testing; 1: future-testing), 
               error type ("ETQ": Ex. post tracking quality; "MSE": MeanSquaredError of returns; 
               "MXD": Max. cumulative tracking difference)
        Display: parameters, weights, value and graph of specified tracking error
        Output: specified tracking error
    """
    ### Checking inputs
    if (err_type not in ["ETQ","MSE","MXD"]): 
        txt = KeyError("Undefined type of tracking error. Please use one among ['ETQ','MSE','MXD']")
        raise txt
	
    ### Preparation of stock returns data
    stk_ret, ss, ee, si, ei = PrpRet(stk_ret0, opr)
    
    ### Selecting stocks using PCA
    if opr==1:
        pass
    else:
        stk_ret = stk_ret[all_tc]
    
    ### Creating cmp_df to store the returns and NAVs of both index and portfolio, 
    ### and also the tracking error sequence
    dat_lst = list(stk_ret.index)
    dat_cnt = len(dat_lst)
    cmp_df = pd.DataFrame()
    cmp_df["IND Ret"] = stk_ret["S&P"]
    cmp_df["REP Ret"] = np.zeros((dat_cnt,1))
    cmp_df["IND NAV"] = np.ones((dat_cnt,1))
    cmp_df["REP NAV"] = np.ones((dat_cnt,1))
    cmp_df["ETQ"] = np.zeros((dat_cnt,1))
    cmp_df["MSE"] = np.zeros((dat_cnt,1))
    stk_ret = stk_ret.drop("S&P", axis=1)
    stk_nam_lst = list(stk_ret.columns)
    stk_cnt = len(stk_nam_lst)
        
    ### Preparation of weights data
    if opr==1:
        wgt = W
        for rw in range(dat_cnt):
            if sum(wgt.iloc[rw])>1:
                wgt.iloc[rw] = wgt.iloc[rw]/sum(wgt.iloc[rw])
    else:
        wgt = pd.DataFrame(np.random.normal(0.2,0.2,(dat_cnt, stk_cnt)), columns=stk_nam_lst, index=dat_lst) 
        wgt.iloc[:,:] = W
        if sum(W)>1:
            wgt.iloc[:,:] = W/sum(W)
    
    ### Calculating portfolio returns and NAVs
    for rw in range(dat_cnt):
        ### Calculating portfolio returns, taking stock returns and weights as input
        cmp_df["REP Ret"][dat_lst[rw]] = np.matrix(stk_ret.iloc[[rw]]*wgt.iloc[[rw]]).sum()
        if rw>=1:
            u1 = np.matrix(wgt.iloc[[rw]]) - np.matrix(wgt.iloc[[rw-1]])
            u2 = abs(u1).sum()
            cmp_df["REP Ret"][dat_lst[rw]] -= u2*cost_ratio
            if u2>0:
                print("Rebalanced on", dat_lst[rw])
            ### Calculating NAVs of index and portfolio, taking their returns as input
            cmp_df["IND NAV"][dat_lst[rw]] = cmp_df["IND NAV"][dat_lst[rw-1]] * (1+cmp_df["IND Ret"][dat_lst[rw]])
            cmp_df["REP NAV"][dat_lst[rw]] = cmp_df["REP NAV"][dat_lst[rw-1]] * (1+cmp_df["REP Ret"][dat_lst[rw]])
    u1 = cmp_df.loc[:,["IND NAV", "REP NAV"]]
    
    ### Plotting portfolio against index
    if opr==1:
        MTimeSerPlot(u1, title="Replicated portfolio VS S&P500 Index", xlabel=(str(si)[0:6]+" ~ "+str(ei)[0:6]))

    ### Dealing with different type of tracking errors
    if err_type=="ETQ":		
        ETQ = 0
        dat_lst = list(cmp_df.index)
        ### Calculating tracking errors， taking NAVs above and the transaction cost setting as input
        for rw in range(dat_cnt):
            etqd = abs(cmp_df["REP NAV"][dat_lst[rw]] - cmp_df["IND NAV"][dat_lst[rw]])
            if rw==0:
                cmp_df["ETQ"][dat_lst[rw]] = etqd
            else:
                	cmp_df["ETQ"][dat_lst[rw]] = 1/(rw+1) *( (rw+1-1) * cmp_df["ETQ"][dat_lst[rw-1]] + 1 * etqd )                
        ETQ = cmp_df["ETQ"][dat_lst[-1]]
        ### Showing tracking error results
        if opr==1:
            print("Ex. post tracking quality (ETQ):", round(ETQ*100,3), "%")   
        return ETQ

    if err_type=="MSE":	
        MSE = 0
        dat_lst = list(cmp_df.index)
        ### Calculating tracking errors， taking NAVs above and the transaction cost setting as input
        for rw in range(dat_cnt):
            msed = (cmp_df["IND Ret"][dat_lst[rw]] - cmp_df["REP Ret"][dat_lst[rw]])**2
            if rw==0:
                cmp_df["MSE"][dat_lst[rw]] = msed
            else:
                cmp_df["MSE"][dat_lst[rw]] = 1/(rw+1) *( (rw+1-1) * cmp_df["MSE"][dat_lst[rw-1]] + 1 * msed )          
        MSE = cmp_df["MSE"][dat_lst[-1]]
        ### Showing tracking error results
        if opr==1:
            print("MeanSquaredError of returns: (", round(MSE**0.5*100,3), "% ) ^2")    
        return MSE

    if err_type=="MXD":	
        MXD = 0
        dat_lst = list(cmp_df.index)
        ### Calculating tracking errors， taking NAVs above and the transaction cost setting as input
        for rw in range(dat_cnt):   
            cmd = abs(cmp_df["REP NAV"][dat_lst[rw]]/cmp_df["IND NAV"][dat_lst[rw]]-1)
            MXD=cmd if MXD<cmd else MXD
        ### Showing tracking error results
        if opr==1:
            print("Max. cumulative tracking difference:", round(MXD*100,3), "%")  
        return MXD



##############################
        
    
    
### Parameter settings
stk_ret0 = pd.read_csv(DATAPATH+"/mat_logret-Copy.csv")
start_date = "2011/01/01"
end_date = "2017/12/31"
n_components = 20
n = 10
bck_wnd = 1/2
rbl_wnd = 1/4
cost_ratio = 0.05/100
err_typ = "ETQ"
### Showing parameters
print("Parameter settings:")
print("Start date:", start_date)
print("End date:", end_date)
print("Number of components in PCA:", n_components)
print("Number of stocks in replication:", n)
print("Backtesting window for optimization (month):", bck_wnd*12)
print("Rebalance every X months, X=:", rbl_wnd*12)
print("Ratio of transaction costs:", cost_ratio*100, "%")
print("Type of tracking error:", err_typ)



stk_ret0 = pd.read_csv(DATAPATH+"/mat_logret-Copy2.csv")
### Backtesting and calculating the optimized weights on each rebalancing date
dat_lst = [int(x) for x in stk_ret0["Date"]]
stk_nam_lst = stk_ret0.columns[2:]
stk_cnt = len(stk_nam_lst)
rbl_lst, bck_lst, nrb = GnrDate(start_date, end_date, rbl_wnd, bck_wnd)
w_lst = []
sss, eee = 0, 0
t0 = time.clock()
for i in range(nrb):
    sss = bck_lst[i][0]
    eee = bck_lst[i][1]
    opr = 0
    stk_ret1, u1, u2, u3, u4 = PrpRet(stk_ret0,0)
    all_tc = Pca(stk_ret1)
    tc = all_tc[1:]
    print("Backtesting:", round((i+1)/nrb*100,1), "%")
    err_type = err_typ
    opw = opt.minimize(TrkErr, [0.01]*n, args=(opr,err_type,), bounds=[(0,1)]*n).x
    k = []
    if len(opw) == len(tc):
        for j in range(stk_cnt):
            idc = LstFndInd(tc, stk_nam_lst[j])
            w1 = opw[idc] if idc>=0 else 0
            k.append(w1)
    w_lst.append(k)
W = GnrW(w_lst, rbl_lst, dat_lst, stk_nam_lst)



### Testing with generated weights, constructing portfolio and calculating tracking error
ETQ_real = TrkErr(W, 1, err_typ)
t1 = time.clock()
print("Lead time:", round((t1-t0)/60,2), "minute(s)")
















