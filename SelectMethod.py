

class SelectMethod():
    '''
        define selecting method

        input: historical window data (df)
        output: selected ticker (pd.columns)
    '''
    def select(self):

        raise NotImplementedError(
            "Method not defined from base class")



class TopCap(SelectMethod):

    ''' 
        select components with largest capitalization

        input: 
            df: window capitalization
            n: num of components to be selected

    '''
    def __init__(self, df, n):

        self.df = df 
        self.n = n 
    
    def select(self):
        sort_pool = self.df.sort_values(
            by=self.df.index[0], axis=1, ascending=False)
        return sort_pool.columns[:self.n]
        


class PCA(SelectMethod):

    '''
        select components by PCA method

        input: window returns
    '''
    def __init__(self, df):
    
        self.df =df

    def select(self):

        pass
    