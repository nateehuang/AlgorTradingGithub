'''
Created on Feb 25, 2020

@author: Nate, Zibin, Martin
'''

from PartB.StockStatPlot import oneStockTradeStat, oneStockQuoteStat

if __name__ == '__main__':
    
    plot = False # Change to True if want to plot
    
    if plot == True:
        oneStockTradeStat('AYE', False) # False: before clean
        oneStockTradeStat('AYE', True) # True: after clean
              
        oneStockTradeStat('RRC', False)
        oneStockTradeStat('RRC', True)
          
        oneStockQuoteStat('AYE', False)
        oneStockQuoteStat('AYE', True)
          
        oneStockQuoteStat('RRC', False)
        oneStockQuoteStat('RRC', True)
