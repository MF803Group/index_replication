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
    
    def __check_len(self, other):
        if (self.s.index != other.s.index).any() or \
            len(self.s.index) != len(other.s.index):
            raise ValueError(self.s.index,"!=",other.s.index)

    def __len__(self):
        return len(self.s)

    def plotvs(self, other, label=["portfolio", "index"], 
        kind=["line", "line"], color=["blue", "orange"]):
        '''
            plot one price process against other process
        '''
        self.__check_len(other)

        plt.figure()
        self.s.plot(label=label[0], kind=kind[0], color=color[0])
        other.s.plot(label=label[1], kind=kind[1], color=color[1])
        plt.legend()
        plt.xlabel("Date")
        plt.ylabel("Net Value")
        plt.title("Tracking Performance")
        plt.show()


