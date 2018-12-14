import numpy as np 
import pandas as pd 
from SelectMethod import TopCap, TopCorr, PCA 
from WeightMethod import CapWeight, OptWeight
from Process import PriceProcess
from MultiProcess import WeightProcess
from TrkErrMeasure import ETQ, MAD, available_measure_kind

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
        self.setting(30, 360, 'ETQ', 0.0)

    def setting(self, step, window, measure_kind, trans_ratio):
        self.step = step
        self.window = window
        self.measure_kind = measure_kind
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
                print("Rebalancing ", str(date)[:10])
            
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
            
            if printer == True:
                print("Selected Ticker", list(sel_ticker))
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
                    self.measure_kind,
                    self.trans_ratio
                )
                sel_weight = optweight.weight()
            if printer == True:
                print("Selected Weight", np.round(sel_weight,4))
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

    def __init__(self, n, select, weight):
        self.n = n
        self.select = select
        self.weight = weight
        self.setting(360, 'ETQ', 0.02, 0.0)

    def setting(self, window, measure_kind, threshold, trans_ratio):
        self.window = window
        self.measure_kind = measure_kind
        self.threshold = threshold
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
        if self.measure_kind not in available_measure_kind:
            raise TypeError("measure kind", self.measure_kind, "not supported")
        

    def run(self, printer=True):
        self.__check_data()
        self.__check_method()
        self.port_wgt_proc = WeightProcess()
        self.port_prc_proc = PriceProcess()
        self.index_prc_proc = PriceProcess()

        i = self.window
        while(i < len(self.logret)):
            date = self.logret.index[i]
            if printer == True: 
                print("Rebalancing ", str(date)[:10])
            
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
            
            if printer == True:
                print("Selected Ticker", list(sel_ticker))
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
                    self.measure_kind,
                    self.trans_ratio
                )
                sel_weight = optweight.weight()
            if printer == True:
                print("Selected Weight", np.round(sel_weight,4))
            temp_port_wgt_proc = WeightProcess(date, sel_ticker, sel_weight)
            self.port_wgt_proc.append(temp_port_wgt_proc)
            
            temp_index_prc_proc = PriceProcess()
            temp_port_prc_proc = PriceProcess()
            
            trk_err = 0.0
            while (trk_err <= self.threshold and i < len(self.logret)):

                date = self.logret.index[i]
                # ----- holding period ----- #
                step_index_ret = self.logret[i:i+1, 0]
                temp_index_prc_proc.append(np.exp(step_index_ret))

                step_port_ret = self.logret[i:i+1][sel_ticker]
                temp_port_prc_proc.append((
                    sel_weight * np.exp(step_port_ret)
                ).agg('sum', axis=1))

                if self.measure_kind == 'ETQ':
                    trk_err = ETQ(temp_index_prc_proc.s, temp_port_prc_proc.s)
                elif self.measure_kind == 'MAD':
                    trk_err = MAD(temp_index_prc_proc.s, temp_port_prc_proc.s)

                if printer == True:
                    print(str(date)[:10], "track error:" ,np.round(trk_err,4))
                i += 1
       
        self.index_prc_proc.append(temp_index_prc_proc.s)
        self.port_prc_proc.append(temp_port_prc_proc.s)

    def evalute(self):

        pass
    pass

