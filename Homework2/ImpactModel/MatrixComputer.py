'''
Created on Mar 7, 2020

@author: guanyuyao
'''

from LeeCode.ReturnBuckets import ReturnBuckets
from LeeCode.TickTest import TickTest
from LeeCode.VWAP import VWAP
from datetime import datetime
import numpy as np

class MatrixComputer(object):
    '''
    Class used to compute all data needed
    '''

    def __init__(self, dailyData):
        
        self._data = dailyData
        self._dataLen = dailyData.getN() # total trade/quote
        self._timeStart = dailyData.getTimestamp(0) # first timestamp
        self._timeEnd = dailyData.getTimestamp(self._dataLen - 1) # last timestamp
        
    def computeTwoMinReturns(self):
        
        timeInterval = 2 * 60 * 1000 # Two minutes 
        
        numBuckets = int((self._timeEnd - self._timeStart) / timeInterval ) # number of buckets
        
        RB = ReturnBuckets(self._data, self._timeStart, self._timeEnd, numBuckets)
        
        return RB.getReturns()
        
    
    def computeTotalDailyVolume(self):
        
        return np.sum(np.array(self._data.getSizes())) # sum the size list
    
    def computeArrivalPrice(self):
        
        result = 0
        
        for i in range(5):
            
            result += self._data.getPrice(i) # average of the first 5 prices
        
        return (result / 5)
    
    def computeImbalance(self):
        
        # value of imbalance from 9:30 to 15:30
        # value of imbalance = number of shares * vwap330
        
        tm330 = datetime.fromtimestamp(self._timeEnd/1000)
        
        tm330 = tm330.replace(hour=15, minute=30, second=0)
        
        tm330 = tm330.timestamp() * 1000 # time stamp for 15:30 
        
        tt = TickTest()
        
        # classify the direction of trade
        tickResult = np.array(tt.classifyAll(self._data, self._timeStart, tm330 + 1000))
        
        tick = tickResult.T[2]
        
        size = tickResult.T[3]
        
        shares = np.sum(np.multiply(tick, size)) # sum the size until 15:30
        
        return shares * self.computeVWAP330()
    
    def computeTerminalPrice(self):
        
        result = 0
        
        for i in range(5):
            
            result += self._data.getPrice(self._dataLen - i - 1) # average of last 5 prices
        
        return (result / 5)
    
    def computeVWAP400(self):
        # (price * corresponding number of shares) / total number of shares
        return VWAP(self._data, self._timeStart, self._timeEnd + 1000).getVWAP()
    
    def computeVWAP330(self):
        
        tm330 = datetime.fromtimestamp(self._timeEnd/1000)
        
        tm330 = tm330.replace(hour=15, minute=30, second=0)
        
        tm330 = tm330.timestamp() * 1000
        
        return VWAP(self._data, self._timeStart, tm330 + 1000).getVWAP()