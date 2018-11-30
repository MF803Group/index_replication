import numpy as np 


class TrackError():

    pass


class ETQ(TrackError):
    '''
        caculate track error between two price process
    ''' 

    def __init__(self, s1, s2):
        self.s1 = s1 
        self.s2 = s2
        self.__check_len()

    def __check_len(self):
        if len(self.s1) != len(self.s2):
            raise ValueError("length of s1: ", len(self.s1),
                " is not equal to s2: ", len(self.s2))
    
    def calculate(self):
        np.sum(np.abs(self.s1 - self.s2)) / len(self.s1)



