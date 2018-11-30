import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from setting import DATAPATH
from MatData import MatData


df = pd.read_csv(DATAPATH+'mat_close.csv')
close = MatData(df)
