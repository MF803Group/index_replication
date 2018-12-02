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
index_prc_proc = PriceProcess()
index_prc_proc.append(temp_index_prc_proc)
port_prc_proc.plotvs(index_prc_proc)
port_prc_proc.trk_err_vs(index_prc_proc)
```
