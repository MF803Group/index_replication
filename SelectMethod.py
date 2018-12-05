import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA as pca
from sklearn.linear_model import LinearRegression

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

    def select(self, n, n_components=20):
        
        # drop stocks that are not listed, and save stock index in a dict
        self.df = self.df.dropna(axis=1,how='any')
        ticker_name = self.df.columns
        ticker_dict = {x: y for x, y in enumerate(ticker_name)}
            
        # construct the pca model and fit the model with data
        sample = self.df.values
        model = pca(n_components=n_components)
        model.fit(sample)
        
        # compute PCA components and corresponding variance ratio
        pcs = model.components_
        pcs_mat = np.matrix(pcs)
        var_ratio = model.explained_variance_ratio_
        var_ratio_mat = np.matrix(var_ratio)
        
        # compute overall loadings for each stock
        load_mat = var_ratio_mat*pcs_mat
        
        # find top 20 stocks with largest loadings
        load_arr = np.asarray(load_mat).reshape(-1)
        load_dict = {y: x for x, y in enumerate(load_arr)}
        sort_load = sorted(load_arr, key=abs, reverse=True)
        top_load = sort_load[:n]
        ticker_num = [load_dict[x] for x in top_load]
        selected_ticker = [ticker_dict[x] for x in ticker_num]
        
        return selected_ticker

class TopCorr(SelectMethod):

    '''
        select components by PCA method

        input: window returns
    '''
    def __init__(self, df):
    
        self.df =df

    def select(self, n):
        
        # preprocess the dataframe
        self.df = self.df.dropna(axis=1, how='any')
        ticker = self.df.columns
        ticker_dict = {x: y for x, y in enumerate(ticker)}
        
        # run regressions for each stock w.r.t. S&P 500
        corr_list = []
        for ticker in ticker[1:]:
            X_series = self.df[ticker].dropna()
            X = X_series.values.reshape(-1,1)
            y = self.df.loc[X_series.index, 'S&P'].values.reshape(-1,1)
            corr_temp = np.correlate(X.flatten(),y.flatten())
            corr_list.append(corr_temp[0])
        
        # get the top n corrs
        corr_dict = {y: x for x, y in enumerate(corr_list)}
        sort_corr = sorted(corr_list, key=abs, reverse=True)
        top_corr = sort_corr[:n]
        corr_index = [corr_dict[x] for x in top_corr]
        selected_ticker = [ticker_dict[x] for x in corr_index]
        
        return selected_ticker
    