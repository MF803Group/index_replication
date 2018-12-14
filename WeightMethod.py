import numpy as np 
import pandas as pd
from scipy.optimize import minimize
from MultiProcess import WeightProcess
from TrkErrMeasure import ETQ

class WeightMethod():
    '''
        define weighting method

        input: 
            historical window data of 
                selected components(MatData)
    
        output: 
            shares (np.arrays)

    '''
    def weight(self):

        raise NotImplementedError(
            "Method not defined from base class")



class CapWeight(WeightMethod):

    ''' 
        weighting components by capitalization
    '''
    def __init__(self, df):

        self.df = df 
    
    def weight(self):
        return self.df / np.sum(self.df.values)


class OptWeight(WeightMethod):

    '''
        weighting components by minimizing track error

        parameters:
            port: optimizing window of portfolio logret
            index: optimizing window of index logret, 
            wgtproc: weight process dating up to now
            transcost: tranaction cost due to weight changes
    '''
    def __init__(self, pool, index, wgtproc, trans_ratio):

        self.pool = pool
        self.index = index
        self.wgtproc = wgtproc
        self.trans_ratio= trans_ratio
        if len(pool) != len(index):
            raise ValueError("length of fisrt window:",len(pool),
                "!= length of second window:", len(index))
        self.lastdate = index.index[-1]
        self.ticker = list(pool.columns)

    def measure_func(self, w, pool_proc, index_proc):
        '''
            w: weights (n by 1 array)
            pool_proc: pool price process
            index_proc: index price process
        '''
        port_proc = (pool_proc * w).apply(sum, axis=1)
        new_wgt = WeightProcess(date=self.lastdate, ticker=self.ticker, weight=w)
        old_wgt = self.wgtproc[-1]
        transcost = new_wgt.get_delta(old_wgt) * self.trans_ratio
        port_proc.iloc[-1] = port_proc.iloc[-1] - transcost
        etq = ETQ(port_proc, index_proc)
        return etq

    def weight(self):

        pool_proc = np.exp(self.pool.cumsum())
        index_proc = np.exp(self.index.cumsum())

        w0 = np.array([0.1]*10)
        w_constraint = ({'type': 'eq', 'fun': lambda w: sum(w) - 1.})
        res = minimize(self.measure_func, w0, 
            args=(pool_proc,index_proc),
            constraints=w_constraint)

        return res.x
    