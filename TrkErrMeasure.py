import numpy as np
import pandas as pd

available_measure_kind = ['ETQ', 'MAD']

def ETQ(port_proc, index_proc, kind = "logret"):
    '''
        kind = "logret"
        port_proc: portfolio logret process
        index_proc: index logret process
        
        kind = "price"
        port_proc: portfolio price process
        index_proc: index price process
    '''
    if len(port_proc) != len(index_proc):
        raise ValueError("length of fisrt process:",len(port_proc),
            "!= length of second process:", len(index_proc))
    T = len(index_proc)
    if kind == "logret":
        port_prc_proc = np.exp(port_proc.cumsum())
        index_prc_proc = np.exp(index_proc.cumsum())
        etq = (port_prc_proc - index_prc_proc).apply(abs).values.sum()*(1/T)
        return etq
    elif kind == "price":
        etq = (port_proc - index_proc).apply(abs).values.sum()*(1/T)
        return etq
    else:
        raise TypeError("kind ", kind, "not supported")

def MAD(port_proc, index_proc, kind="logret"):
    '''
        kind = "logret"
        port_proc: portfolio logret process
        index_proc: index logret process
        
        kind = "price"
        port_proc: portfolio price process
        index_proc: index price process
    '''
    if len(port_proc) != len(index_proc):
        raise ValueError("length of fisrt process:",len(port_proc),
            "!= length of second process:", len(index_proc))
    T = len(index_proc)
    if kind == "logret":
        mad = (port_proc - index_proc).apply(abs).values.sum()*(1/T)
        return mad
    elif kind == "price":
        port_ret_proc = port_proc.apply(np.log).diff().dropna()
        index_ret_proc = index_proc.apply(np.log).diff().dropna()
        mad = (port_ret_proc - index_ret_proc).apply(abs).values.sum()*(1/T)
        return mad
    else:
        raise TypeError("kind ", kind, "not supported")        
