'''
Created on Feb 24, 2020

@author: furonghuang
'''
import os
import numpy as np
from PartC.TradeReturn import TradeReturn
from statsmodels.stats.diagnostic import acorr_ljungbox

if __name__ == '__main__':
    # find the path of the binary files of the trade data
    parentPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    # directory of the trade files
    filePath = os.path.join(parentPath, "clean_trades")
    
    test_lag = []
    # The lags we want to test, from 30 seconds to 60 minutes
    lags = [30000, 60000, 120000, 300000, 600000, 1200000, 1800000, 3600000]
    # The tickers we want to test
    tickers = ["MS", "RRC", "GILD", "USB", "MDP", "NBL", "AYE", "MU", "COV", "AAPL", "C", "WLP", "NE"]
    # instantiate a TradeReturn, pass in the directory of the trade files
    trRe = TradeReturn(filePath)
    # loop through the ticker in the tickers list to find the optimal lag
    for tick in tickers:
        print("Finding the best lag for ", tick)
        # loop through the lags list to test
        for lag in lags:
            # calculate the return of the trade files
            re = trRe.GetReturn(tick, lag)
            # calculate the p value 
            _, pv = acorr_ljungbox(re, 1, return_df = False)
            # if the p value is greater than 0.05, determine the time is a good lag and break the loop
            if pv > 0.01:
                print("For ", tick, lag/60000, "minutes is a good time lag")
                test_lag.append(lag)
                break
    
    #print("The average best lag time is ", np.mean(test_lag)/60000, "minutes is a good time lag")