import pandas as pd 
import matplotlib.pyplot as plt

class PriceProcess():

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