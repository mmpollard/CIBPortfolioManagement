import numpy as np
import pandas as pd
import math
import scipy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import os


pd.options.display.mpl_style = 'default'
pylab.rcParams['figure.figsize'] = 12, 6




def strat1(ticker):
    def get(ticker):
        temp_df = pd.read_csv("https://www.quandl.com/api/v3/datasets/YAHOO/"+ticker+".csv")
        temp_df.index = pd.to_datetime(temp_df.Date)
        temp_df = temp_df.sort()
        return temp_df
    ret_df = get(ticker)
    ret_df['ret'] = ret_df.Close.shift(-1) - ret_df.Close
    return_df = ret_df
    return_df['day1'] = np.where(return_df.ret > return_df.ret.shift(1), 1, 0)
    return_df['five_days'] = np.where(return_df.day1 + return_df.day1.shift(1) +
                                 return_df.day1.shift(2) + return_df.day1.shift(3) +
                                 return_df.day1.shift(4) + return_df.day1.shift(5) == 5, 1, 0)
    return_df['trade_yes'] = np.where(return_df.five_days == 1, 1, 0)
    return_df['ret_long'] = np.where(return_df.trade_yes == 1, return_df.ret + return_df.ret.shift(-1) +
                                 return_df.ret.shift(-2) + return_df.ret.shift(-3) +
                                 return_df.ret.shift(-4) + return_df.ret.shift(-5), 0)
    return_df['ret_short'] = -1 * return_df.ret_long
    return_df = return_df[return_df.index.year > 2000]
    length = return_df.ret_long.size / 15
    sharpe_df = return_df.ret_long.cumsum()[::length].shift(-1) - return_df.ret_long.cumsum()[::length]
    yearly_sharpe = sharpe_df.mean() / sharpe_df.std()
    return_df.ret_long.cumsum().plot(title = ticker+ "\n--Five Day Trade--\nSharpe = " + str(yearly_sharpe));
    return return_df
