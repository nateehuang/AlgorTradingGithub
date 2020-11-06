'''
Created on Feb 22, 2020
@author: Nate, Zibin, Martin

'''
import os
import numpy as np
import matplotlib.pyplot as plt
from PartA.TAQAdjust import Adjuster
from PartA.TAQCleaner import CleanTAQ

if __name__ == '__main__':
    
    ad = Adjuster()
    # filter SP500 stocks
    ad.filterSP500()
    
    # set save=True to save the file after adjusting
    print("Start adjusting data")
    ad.adjust(save=False)
    
    # Analysis 
    # change analyze to True to do the analysis
    analyze = False
    if analyze:
        # Assume that there is around 3% data are outliners
        percent = []
        # subset across tickers with different number of records
        tickerLs = ["MDT", "KR", "AA", "HAL", "AAPL"]
        print("Start to search for good parameter for cleaning procedure")
        ks = [0.0005, 0.00005, 0.000005, 0.0000005]
        ils = []
        for i in range(5, 10):
            coeff = []
            for c in ks:
                tick_per = np.zeros(len(tickerLs))
                print("k=", i , "coeffcient=", c)
                for j, t in enumerate(tickerLs):
                    cl = CleanTAQ(os.path.join(os.getcwd(), "adjusted_trades"), k=i, gCoeff=c)
                    # Only one day subset of the data will be used for analysis
                    count, _, p = cl.clean_trades(t, subset=True, save=False)
                    tick_per[j] = float(len(p)*65)/count
                coeff.append(tick_per.mean())
            ils.append(coeff)
        print(ils)
        i = 5
        for thing in ils:
            plt.plot(np.log(ks), thing, '.', label =i)
            plt.legend()
            i+=1
        plt.xlabel("Gamma Coefficient in log scale")
        plt.ylabel("Percentage retain")
        plt.legend()
        plt.title("Trade clean filter ratio with different parameter")
        plt.show()
        
        for i in range(5, 10):
            coeff = []
            for c in ks:
                tick_per = np.zeros(len(tickerLs))
                print("k=", i , "coeffcient=", c)
                for j, t in enumerate(tickerLs):
                    cl = CleanTAQ(os.path.join(os.getcwd(), "adjusted_quotes"), k=i, gCoeff=c)
                    # Only one day subset of the data will be used for analysis
                    count, _, p, p_ = cl.clean_quotes(t, subset=True, save=False)
                    tick_per[j] = float(len(p)*65)/count
                coeff.append(tick_per.mean())
            ils.append(coeff)
        print(ils)
        i = 5
        for thing in ils:
            plt.plot(np.log(ks), thing, '.', label =i)
            plt.legend()
            i+=1
        plt.xlabel("Gamma Coefficient in log scale")
        plt.ylabel("Percentage retain")
        plt.legend()
        plt.title("Quote clean filter ratio with different parameter")
        plt.show()
        
    
    # For trades, k=8, Gamma Coefficient = 0.00005 ~ 1e-5 screen out around 3% data
    # For quotes, k=6, Gamma Coefficient = 0.000005 ~ 1e-6 screen out around 3% data
    
    # Now clean the adjusted trade data
    # if want to save data into files, change save_clean to True
    save_clean = False
    print("Clean Adjusted Trades Data")
 
    ad_trade_path = os.path.join(os.getcwd(), "adjusted_trades")
    cltr = CleanTAQ(ad_trade_path, k=8, gCoeff=0.00005)
    tr_ls = os.listdir(ad_trade_path)
    tr_ls.sort()
    for tick in tr_ls:
        if tick.endswith("_trades.gz"):
            cltr.clean_trades(tick[:-10], subset=False, save=save_clean)
    
    # Now clean the adjusted quotes data
    print("Clean Adjusted Quotes Data")
    ad_quote_path = os.path.join(os.getcwd(), "adjusted_quotes")
    clqu = CleanTAQ(ad_quote_path, k=6, gCoeff=0.000005)
    qu_ls = os.listdir(ad_quote_path)
    qu_ls.sort()
    for tick in qu_ls:
        if tick.endswith("_quotes.gz"):
            clqu.clean_quotes(tick[:-10], subset=False, save=save_clean)
    
    
        
        
        
                