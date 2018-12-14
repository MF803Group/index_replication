import numpy as np
import pandas as pd


def ETQ(port_proc, index_proc):
    '''
        port_proc: portfolio price process
        index_proc: index price process
    '''
    if len(port_proc) != len(index_proc):
        raise ValueError("length of fisrt process:",len(port_proc),
            "!= length of second process:", len(index_proc))
    T = len(index_proc)
    etq = (port_proc - index_proc).apply(abs).values.sum()*(1/T)
    return etq