# Documentation

# Class
## MatData
class MatData(df=None)
    
* define a matrix data, index: Date(pd.DatatimeIndex), columns: Ticker(str)

* parameters:
    
    df: pd.Dataframe
```
matdata = MatData(pd.read_csv('hist_cap.csv'))
```
## Process
class PriceProcess(s=None)
    
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
class WeightProcess(df=None)
    
* define multiple time series process

* parameters:
    
    df: pd.DataFrame

* methods:
    
    append.(WeightProcess): combine two weight process

## SelectMethod
class TopCap(df=None)
    
* define a method of selecting n components of top capitalization

* parameters:
    
    df: pd.DataFrame

* methods:
    
    select.(): output selected tickers (pd.Index)
```
topcap = TopCap()
```
class PCA(df=None)

* define a method of selecting n components by Principle Component Analysis(PCA)

* parameters:
    
    df: pd.DataFrame

* methods:
    
    select.(): output selected tickers (pd.Index)
```
pca = PCA()
```

## WeightMethod
class CapWeight(df=None)
    
* define a method of weighting components by their capitalization

* parameters:
    
    df: pd.DataFrame

* methods:
    
    weight.(): output weights of tickers (WeightProcess)
```
capweight = CapWeight()
```
