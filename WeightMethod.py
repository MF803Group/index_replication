import numpy as np 
import pandas as pd
from scipy.optimize import minimize
from MultiProcess import WeightProcess
from TrkErrMeasure import ETQ, MAD, available_measure_kind

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
    def __init__(self, pool, index, wgtproc, measure_kind, trans_ratio):

        self.pool = pool
        self.index = index
        self.wgtproc = wgtproc
        self.measure_kind = measure_kind
        self.trans_ratio= trans_ratio
        self.lastdate = index.index[-1]
        self.ticker = list(pool.columns)
        self.__checking()

    def __checking(self):
        if len(self.pool) != len(self.index):
            raise ValueError("length of fisrt window:",len(self.pool),
                "!= length of second window:", len(self.index))
        if self.measure_kind not in available_measure_kind:
            raise TypeError("measure kind:", self.measure_kind,"not supported")

    def measure_func(self, w, pool_proc, index_proc, measure_kind):
        '''
            w: weights (n by 1 array)
            pool_proc: pool logret process
            index_proc: index logret process
        '''
        port_proc = (pool_proc * w).apply(sum, axis=1)
        new_wgt = WeightProcess(date=self.lastdate, ticker=self.ticker, weight=w)
        old_wgt = self.wgtproc[-1]
        transcost = new_wgt.get_delta(old_wgt) * self.trans_ratio
        port_proc.iloc[-1] = port_proc.iloc[-1] - transcost
        if measure_kind == 'ETQ':
            return ETQ(port_proc, index_proc)
        elif measure_kind == 'MAD':
            return MAD(port_proc, index_proc)

    def weight(self):

        w0 = np.array([0.1]*10)
        w_constraint = ({'type': 'eq', 'fun': lambda w: sum(w) - 1.})
        res = minimize(self.measure_func, w0, 
            args=(self.pool,self.index,self.measure_kind),
            constraints=w_constraint)

        return res.x
    