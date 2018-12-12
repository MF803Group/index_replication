# Documentation

# Class
## MatData
class MatData(df=None)
    
* define a matrix data, index: Date(pd.DatatimeIndex), columns: Ticker(str)

* parameters:
    
    df: pd.Dataframe

* method:
    
    index_setting.(): set Date as index
```
matdata = MatData(pd.read_csv('hist_cap.csv'))

matdata.index_setting.()
```
## Process
class Process():

* define a time series process

* parameters:

    s: pd.Series

class PriceProcess(Process)
    
* define single time series process

* parameters:
    
    s: pd.Series

* methods:
    
    append.(PriceProcess): combine two price process
    
    plotvs.(PriceProcess): plot one price process against another
    
    trk_err_vs.(PriceProcess): return tracking error(TrakcErrProcess) 
        of two price process

```
one_process = PriceProcess()

one_process.append(other_process)

one_process.plotvs(index_process)

one_process.trk_err_vs(index_process)
```
## MultiProcess

class MultiProcess():

* define multi time series process

* parameters:
    
    df: pd.DataFrame

class WeightProcess(MultiProcess)
    
* define multiple time series process

* parameters:
    
    df: pd.DataFrame

* methods:
    
    append.(WeightProcess): combine two weight process

## SelectMethod
class SelectMethod()

* define a selecting method

* parameters:

    matdata: MatData

* methods:
    
    select.(): return selected tickers (pd.Index)
    
class TopCap(SelectMethod)
    
* define a method of selecting n components of top capitalization

class TopCorr(SelectMethod):

* define a method of selecting based on correlation w.r.t index

class PCA(SelectMethod)

* define a method of selecting by using Principle Component Analysis

```
from SelectMethod import PCA

pca = PCA(matdata)

selected_ticker = pca.select()
```

## WeightMethod

class WeightMethod():

* define a weighting method

* parameters:
    
    matdata: MatData
    
* methods:
    
    weight.(): return weights of tickers (WeightProcess)

class CapWeight(WeightMethod)
    
* define a method of weighting components by their capitalization

class OptWeight(WeightMethod)

* define a method of weighting by solving optimization problem


```
from WeightMethod import OptWeight

capweight = CapWeight(matdata)

ticker_weights = capweight.weight()
```
