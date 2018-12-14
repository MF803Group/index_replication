import numpy as np
import pandas as pd

available_measure_kind = ['ETQ', 'MAD']

def ETQ(port_proc, index_proc):
    '''
        port_proc: portfolio logret process
        index_proc: index logret process
    '''
    if len(port_proc) != len(index_proc):
        raise ValueError("length of fisrt process:",len(port_proc),
            "!= length of second process:", len(index_proc))
    T = len(index_proc)
    port_prc_proc = np.exp(port_proc.cumsum())
    index_prc_proc = np.exp(index_proc.cumsum())
    etq = (port_prc_proc - index_prc_proc).apply(abs).values.sum()*(1/T)
    return etq

def MAD(port_proc, index_proc):
    '''
        port_proc: portfolio logret process
        index_proc: index logret process
    '''
    if len(port_proc) != len(index_proc):
        raise ValueError("length of fisrt process:",len(port_proc),
            "!= length of second process:", len(index_proc))
    T = len(index_proc)
    mad = (port_proc - index_proc).apply(abs).values.sum()*(1/T)
    return mad
