import numpy as np 

class WeightMethod():
    '''
        define weighting method

        input: 
            historical window data of 
                selected components(MatData)
    
        output: 
            shares (np.arrays)

    '''
    def weight(self):

        raise NotImplementedError(
            "Method not defined from base class")



class CapWeight(WeightMethod):

    ''' 
        weighting components by capitalization
    '''
    def __init__(self, df):

        self.df = df 
    
    def weight(self):
        return self.df / np.sum(self.df.values)


class MinTrackError(WeightMethod):

    '''
        weighting components by minimizing track error
    '''
    def __init__(self, df):
    
        self.df = df

    def weight(self):
        pass
    