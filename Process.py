import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt


class Process():
    '''
        define a time series process
    '''

    def append(self, time_series):
        raise NotImplementedError(
            "method not defined for base class")

class PriceProcess(Process):

    def __init__(self, s=pd.Series()):
        self.s = s

    def append(self, s):
        '''
            extend two price process
        '''
        if len(self.s) == 0:
            self.s = self.s.append(s)
        else:
            adj_factor = self.s[-1] / 1
            s = s * adj_factor
            self.s = self.s.append(s)
    
    def __check_len(self, prcproc):
        if (self.s.index != prcproc.s.index).any() or \
            len(self.s.index) != len(prcproc.s.index):
            raise ValueError(self.s.index,"!=",prcproc.s.index)

    def plotvs(self, prcproc, col=["grey", "black"],lgd_loc="upper left"):
        '''
            plot port price process against 
            index price process
        '''
        self.__check_len(prcproc)
        fig = plt.figure()
        fig1 = fig.add_subplot(1,1,1)
        fig1.plot(self.s.index, self.s, color=col[0], label="index")
        fig1.plot(self.s.index, prcproc.s, color=col[1], label="portfolio")
        plt.legend(loc=lgd_loc)
        fig1.set_title("tracking portfolio vs index")
        start_date = str(self.s.index[0].year) + str(self.s.index[0].month)
        end_date = str(self.s.index[-1].year) + str(self.s.index[-1].month)
        fig1.set_xlabel(start_date + "~" + end_date)
        fig1.set_xticks([])
        plt.show()
    
    def trk_err_vs(self, prcproc, kind='ETQ'):
        '''
            calculate tracking error against 
            index price process
            output: tracking error process
        '''
        self.__check_len(prcproc)
        if kind == 'ETQ':
            s = pd.Series(data=np.abs(self.s - prcproc.s), index=self.s.index)
            return TrackErrProcess(s)

class TrackErrProcess(Process):
    def __init__(self, s=pd.Series()):
        self.s = s 

