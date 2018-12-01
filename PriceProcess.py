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

    def plotvs(self, s):
        '''
            plot port price process against 
            index price process
        '''
        plt.figure()
        self.s.name = "tracking portfolio"
        self.s.plot()
        s.s.name = "index"
        s.s.plot()
        plt.legend()
        plt.show()

class ShareProcess(Process):

    def __init__(self, df=pd.DataFrame()):
        self.df = df 
    
    def append(self, df):
        self.df = self.df.append(df)