'''
Created on Feb 24, 2020

@author: Zibin
'''
from PartB.TAQStats import TAQStats
import matplotlib.pyplot as plt
import numpy as np
import os

''' Function to compute trade basic statistic of one stock'''
def oneStockTradeStat(ticker1, isClean, ty = 'trades'):
    
    parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)) # parent directory
        
    if isClean:
        path = parentddir + '/clean_trades/' + ticker1 + '_trades.gz'
    else:
        path = parentddir + '/PartA/adjusted_trades/' + ticker1 + '_trades.gz'
    
    stat = TAQStats(path, ty) # Create an object
   
    # retrieve statistics
    mean1, median1, std1, mad1, skew1, kurt1, large1, small1, maxdd1 = stat.tradeReturnStat()
    print(mean1)
    print(median1)
    print(std1)
    print(mad1)
    print(skew1)
    print(kurt1)
    print(maxdd1)
    
    plt.title('Trade Return Statistics of ' + ticker1)
    x = ['mean', 'median', 'std', 'MAD', 'skew', 'kurt', 'maxDdown']
    y1 = [mean1, median1, std1, mad1, skew1, kurt1, maxdd1]
    plt.plot(x, y1, '-o', color = 'black')
    plt.show()
    
    plt.title('10 Largest and Smallest Trade Returns of ' + ticker1)
    plt.plot(np.arange(len(large1)), large1, '-o', color = 'black', label = ticker1 + ' Trade Largest')
    plt.plot(np.arange(len(small1)), small1, '-o', color = 'y', label = ticker1 + ' Trade Smallest')
    plt.legend()
    plt.show()

''' Function to compute quote basic statistic of one stock'''   
def oneStockQuoteStat(ticker1, isClean, ty = 'quotes'):
    parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)) # parent directory
        
    if isClean:
        path = parentddir + '/clean_quotes/' + ticker1 + '_quotes.gz'
    else:
        path = parentddir + '/PartA/adjusted_quotes/' + ticker1 + '_quotes.gz'
    
    stat = TAQStats(path, ty) # Create an object
    
    # retrieve statistics
    mean1, median1, std1, mad1, skew1, kurt1, large1, small1, maxdd1 = stat.midQuoteReturnStat()
    
    plt.title('Mid-Quote Statistics of ' + ticker1)
    x = ['mean', 'median', 'std', 'MAD', 'skew', 'kurt', 'maxDdown']
    y1 = [mean1, median1, std1, mad1, skew1, kurt1, maxdd1]
    plt.plot(x, y1, '-o', color = 'black')
    plt.show()
    
    plt.title('10 Largest and Smallest Mid-Quote Returns of ' + ticker1)
    plt.plot(np.arange(len(large1)), large1, '-o', color = 'black', label = ticker1 + ' Quote Largest')
    plt.plot(np.arange(len(small1)), small1, '-o', color = 'y', label = ticker1 + ' Quote Smallest')
    plt.legend()
    plt.show()

# ''' Function to compare trade basic statistic of two stocks'''
# def stockStatTradeCompare(ticker1, ticker2, isClean):
#     stat = TAQStats(isClean)
#     
#     plt.title('Number of Trades and Number of Quotes')
#     plt.plot('numTrade', numTrade1, marker = 'o', ms = 10, color = 'black', label = ticker1 + ' Trade')
#     plt.plot('numQuote', numQuote1, marker = 'x', ms = 10, color = 'black', label = ticker1 + ' Quote')
#     plt.plot('numTrade', numTrade2, marker = 'o', ms = 10, color = 'y', label = ticker2 + ' Trade')
#     plt.plot('numQuote', numQuote2, marker = 'x', ms = 10, color = 'y', label = ticker2 + ' Quote')
#     plt.legend()
#     plt.show()
#     
#     # retrieve statistics of the two stocks
#     mean1, median1, std1, mad1, skew1, kurt1, large1, small1, maxdd1 = stat.tradeReturnStat(ticker1)
#     mean2, median2, std2, mad2, skew2, kurt2, large2, small2, maxdd2 = stat.tradeReturnStat(ticker2)
#     
#     # Plot statistics
#     plt.title('Trade Statistics Comparison btw ' + ticker1 + ' and ' + ticker2)
#     x = ['mean', 'median', 'std', 'MAD', 'skew', 'kurt', 'maxDdown']
#     y1 = [mean1, median1, std1, mad1, skew1, kurt1, maxdd1]
#     y2 = [mean2, median2, std2, mad2, skew2, kurt2, maxdd2]
#     plt.plot(x, y1, '-o', color = 'black', label = ticker1 + ' Trade Stat')
#     plt.plot(x, y2, '-o', color = 'y', label = ticker2+ ' Trade Stat')
#     plt.legend()
#     plt.show()
#     
#     # Plot 10 largest returns 
#     plt.title('10 Largest Trade Returns of ' + ticker1 + ' vs ' + ticker2)
#     plt.plot(np.arange(len(large1)), large1, '-o', color = 'black', label = ticker1 + ' Trade Largest')
#     plt.plot(np.arange(len(large2)), large2, '-o', color = 'y', label = ticker2 + ' Trade Largest')
#     plt.legend()
#     plt.show()
#     
#     plt.title('10 Smallest Trade Returns of ' + ticker1 + ' vs ' + ticker2)
#     plt.plot(np.arange(len(small1)), small1, '-o', color = 'black', label = ticker1 + ' Trade Smallest')
#     plt.plot(np.arange(len(small2)), small2, '-o', color = 'y', label = ticker2 + ' Trade Smallest')
#     plt.legend()
#     plt.show()
# 
# ''' Function to compare quote basic statistic of two stocks'''    
# def stockStatQuoteCompare(ticker1, ticker2, isClean):
#     stat = TAQStats(isClean)
#     
#     mean1, median1, std1, mad1, skew1, kurt1, large1, small1, maxdd1 = stat.midQuoteReturnStat(ticker1)
#     mean2, median2, std2, mad2, skew2, kurt2, large2, small2, maxdd2 = stat.midQuoteReturnStat(ticker2)
#     
#     plt.title('Mid-Quote Statistics Comparison btw ' + ticker1 + ' and ' + ticker2)
#     x = ['mean', 'median', 'std', 'MAD', 'skew', 'kurt', 'maxDdown']
#     y1 = [mean1, median1, std1, mad1, skew1, kurt1, maxdd1]
#     y2 = [mean2, median2, std2, mad2, skew2, kurt2, maxdd2]
#     plt.plot(x, y1, '-o', color = 'black', label = ticker1 + ' Quote Stat')
#     plt.plot(x, y2, '-o', color = 'y', label = ticker2+ ' Quote Stat')
#     plt.legend()
#     plt.show()
#     
#     plt.title('10 Largest Mid-Quote Returns of ' + ticker1 + ' vs ' + ticker2)
#     plt.plot(np.arange(len(large1)), large1, '-o', color = 'black', label = ticker1 + ' Quote Largest')
#     plt.plot(np.arange(len(large2)), large2, '-o', color = 'y', label = ticker2 + ' Quote Largest')
#     plt.legend()
#     plt.show()
#     
#     plt.title('10 Smallest Mid-Quote Returns of ' + ticker1 + ' vs ' + ticker2)
#     plt.plot(np.arange(len(small1)), small1, '-o', color = 'black', label = ticker1 + ' Quote Smallest')
#     plt.plot(np.arange(len(small2)), small2, '-o', color = 'y', label = ticker2 + ' Quote Smallest')
#     plt.legend()
#     plt.show()