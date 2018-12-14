import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt


class MultiProcess():
    '''
        define multi time series process
    '''

    def append(self, time_series):
        raise NotImplementedError(
            "method not defined for base class")

class WeightProcess(MultiProcess):

    def __init__(self, date=None, ticker=None, weight=None):
        if date == None and ticker == None and weight == None:
            self.df = pd.DataFrame()
        elif len(ticker) != weight.size:
            raise ValueError("length of ticker:",len(ticker),
                "!= length of weight:", len(weight))
        else:
            try:
                df = pd.DataFrame(index=pd.date_range(date, periods=1),
                    columns=ticker, data=weight)
            except:
                df = pd.DataFrame(index=pd.date_range(date, periods=1),
                    columns=ticker, data=weight.reshape(1,weight.size))
            self.df = df

    def __getitem__(self, key):
        try:
            subdf = self.df.iloc[key].to_frame().transpose()
        except IndexError:
            return WeightProcess()
        else:
            return WeightProcess(date=subdf.index[0], ticker=list(subdf.columns),
                weight=subdf.values)

    def is_empty(self):
        return self.df.empty
    
    def __len__(self):
        return len(self.df)

    def append(self, other):
        self.df = self.df.append(other.df, sort=False)

    def get_delta(self, other):
        if self.is_empty() and other.is_empty():
            raise ValueError("Can't compute delta of 2 empty WeightProcess")
        elif self.is_empty() and not other.is_empty():
            return other[-1].df.fillna(value=0).values.sum()
        elif not self.is_empty() and other.is_empty():
            return self[-1].df.fillna(value=0).values.sum()
        else:
            delta = self - other
        return delta
    
    def __sub__(self, other):
        if len(self) != 1 or len(other) != 1:
            raise ValueError("length of self:",len(self),
                "or length of other:", len(other), "!=1")
        w1w2 = pd.concat([self.df.squeeze(),other.df.squeeze()],axis=1, sort=False).fillna(value=0)
        return np.abs((w1w2.iloc[:,1] - w1w2.iloc[:,0]).values).sum()