import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from setting import DATAPATH
from MatData import MatData

n = 2

df = pd.read_csv(DATAPATH+'mat_close.csv')
x = MatData(df)
x['Date'] = pd.to_datetime(x['Date'].astype(str))
x.set_index('Date', inplace=True)

df = pd.read_csv(DATAPATH+'mat_ret.csv')
y = MatData(df)
y['Date'] = pd.to_datetime(y['Date'].astype(str))
y.set_index('Date', inplace=True)

# selecing period
mat_pool = x.iloc[:,1:]
vec_index = x.iloc[:,0]
sort_mat_pool = mat_pool[:1].sort_values(by='2010-01-04', axis=1, ascending=False)
sel_pool = mat_pool[:1]
sel_value = sort_mat_pool.values[0,:n]
sel_ticker = sort_mat_pool.columns[:n]
sel_weights = sel_value / np.sum(sel_value)
sel_shares = sel_weights / 1


# holding period
ret_mat_pool = y.iloc[:,1:]
ret_vec_index = y.iloc[:,0]
hold_pool = ret_mat_pool[:(1+10)]
prc_proc = np.exp(hold_pool.cumsum())
port_prc_proc = prc_proc[sel_ticker]
subpool_value_proc = port_prc_proc * sel_shares
port_value_proc = subpool_value_proc.agg('sum', axis=1)

#TODO: price proc 
index_holding_window = ret_vec_index[:(1+10)]
index_proc = np.exp(index_holding_window.cumsum())

plt.figure()
port_value_proc.name = 'tracking portfolio'
port_value_proc.plot()
index_proc.name = 'index'
index_proc.plot()
plt.legend()

plt.show()


