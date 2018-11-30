import pandas as pd 
import matplotlib.pyplot as plt

class PriceProcess():

    def __init__(self, s=pd.Series()):
        self.s = s

    def append(self, s):
        '''
            extend two price process
        '''
    
    def plot(self, s=None):
        if s == None:
            plt.figure()
            self.s.plot()
            plt.legend()
            plt.show()
        else:
            plt.figure()
            self.s.plot()
            s.plot()
            plt.legend()
            plt.show()