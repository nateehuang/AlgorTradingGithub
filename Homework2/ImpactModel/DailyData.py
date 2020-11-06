'''
Created on Mar 7, 2020

@author: guanyuyao
'''

import numpy as np

class DailyData(object):
    '''
    classdocs
    '''
    
    def __init__(self, prices, timestamps, sizes, startIndex, endIndex):
        '''
        Constructor
        '''
        self._prices = prices[startIndex : endIndex]
        self._timestamps = timestamps[startIndex : endIndex]
        self._sizes = sizes[startIndex : endIndex]
        
    def getPrice(self, index):
        
        return self._prices[index]
    
    def getTimestamp(self, index):
        
        return self._timestamps[index]
    
    def getSize(self, index):
        
        return self._sizes[index]
    
    def getN(self):
        
        return len(self._prices)
    
    def getPrices(self):
        
        return self._prices
    
    def getTimestamps(self):
        
        return self._timestamps
    
    def getSizes(self):
        
        return self._sizes
    
    def getNumShares(self):
        
        return (np.array(self._sizes).sum())