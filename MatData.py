import pandas as pd 
from setting import DATAPATH

class MatData():

    def __init__(self, df):
        self.df = self.__index_setting(df)

    def __index_setting(self, df):
        if type(df.index) == pd.DatetimeIndex:
            return df
        elif 'Date' in df.columns:
            df['Date'] = pd.to_datetime(
                df['Date'].astype(str))
            return df.set_index('Date')
        else:
            raise NameError("No columns named Date")             



    
    
        
    
