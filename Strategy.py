import numpy as np 
import pandas as pd 
from SelectMethod import TopCap, TopCorr, PCA 
from WeightMethod import CapWeight, OptWeight
from Process import PriceProcess
from MultiProcess import WeightProcess

available_select_method = ['TopCap', 'TopCorr', 'PCA']
available_weight_method = ['CapWeight', 'OptWeight']

class Strategy():

    def setting(self):
        raise NotImplementedError(
            "Method not defined from base class")

    pass

class CalendarRebalance(Strategy):

    def __init__(self, n, select, weight):
        self.n = n
        self.select = select
        self.weight = weight
        self.setting(30, 360)

    def setting(self, step, window, trans_ratio=0.0):
        self.step = step
        self.window = window
        self.trans_ratio = trans_ratio
    
    def feed(self, *argv, **kwargs):
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == 'logret':
                    self.logret = value
                elif key == 'cap':
                    self.cap = value
                else:
                    raise ValueError("data type not supported")

    def __check_data(self):
        if self.logret == None:
            raise ValueError("logret required")
        if (self.select == 'TopCap' or self.weight == 'CapWeight') and \
            self.cap == None:
            raise ValueError("cap required")

    def __check_method(self):
        if self.select not in available_select_method:
            raise TypeError("select method", self.select, "not supported")
        if self.weight not in available_weight_method:
            raise TypeError("weight method", self.weight, "not supported")

    def run(self, printer=True):
        self.__check_data()
        self.__check_method()
        self.port_wgt_proc = WeightProcess()
        self.port_prc_proc = PriceProcess()
        self.index_prc_proc = PriceProcess()
        for i in range(self.window, len(self.logret)-self.step, self.step):

            date = self.logret.index[i]
            if printer == True: 
                print(date)
            
            # -----  decision period ----- #
            # select

            dec_logret = self.logret[i-self.window:i,:]
            dec_index_logret = self.logret[i-self.window:i,0]

            if self.select == 'TopCap':
                dec_cap = self.cap[i-self.window:i, 1:]
                topcap = TopCap(dec_cap, self.n)
                sel_ticker = topcap.select()
            elif self.select == 'TopCap':
                topcorr = TopCorr(dec_logret)
                sel_ticker = topcorr.select(n=self.n)
            elif self.select == 'PCA': 
                pca = PCA(dec_logret)
                sel_ticker = pca.select(n=self.n)

            print(sel_ticker)
            dec_pool_logret = dec_logret[sel_ticker]
            
            # weight
            if self.weight == 'CapWeight':
                capweight = CapWeight(dec_cap[sel_ticker])
                sel_weight = capweight.weight()
            elif self.weight == "OptWeight":
                optweight = OptWeight(
                    dec_pool_logret, 
                    dec_index_logret, 
                    self.port_wgt_proc,
                    self.trans_ratio
                )
                sel_weight = optweight.weight()

            temp_port_wgt_proc = WeightProcess(date, sel_ticker, sel_weight)
            self.port_wgt_proc.append(temp_port_wgt_proc)
            
            # ----- holding period ----- #
            hold_index_ret = self.logret[i:i+self.step, 0]
            temp_index_prc_proc = (
                np.exp(hold_index_ret.cumsum())
            )
            self.index_prc_proc.append(temp_index_prc_proc)

            hold_port_ret = self.logret[i:i+self.step][sel_ticker]
            temp_port_prc_proc = (
                sel_weight * np.exp(hold_port_ret.cumsum())
            ).agg('sum', axis=1)
            self.port_prc_proc.append(temp_port_prc_proc)
        
        pass

    def evalute(self):

        pass

class ThresholdRebalance(Strategy):

    pass

