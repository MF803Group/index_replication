import pandas as pd 
from setting import DATAPATH

class MatData():
    '''
        define matrix data:
            index: Date(pd.DatatimeIndex)
            columns: Ticker(str)
        
        ex. historical data
            window data

        input: pd.DataFrame 
    '''

    def __init__(self, df):
        self.df = self.__index_setting(df)
        print("initialzing a", len(self.df), 
            "by", len(self.df.columns),"MatData")

    def __index_setting(self, df):
        ''' set Date as index'''
        if type(df.index) == pd.DatetimeIndex:
            return df
        elif 'Date' in df.columns:
            df['Date'] = pd.to_datetime(
                df['Date'].astype(str))
            return df.set_index('Date')
        else:
            raise NameError("No columns named Date")

    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, key):
        return self.df.iloc[key]




    
    
        
    
