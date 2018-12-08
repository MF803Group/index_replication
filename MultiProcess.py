import pandas as pd 
import matplotlib.pyplot as plt


class MultiProcess():
    '''
        define multi time series process
    '''

    def append(self, time_series):
        raise NotImplementedError(
            "method not defined for base class")

class ShareProcess(MultiProcess):

    def __init__(self, df=pd.DataFrame()):
        self.df = df 
    
    def append(self, df):
        self.df = self.df.append(df)