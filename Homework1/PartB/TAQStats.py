'''
Created on Feb 24, 2020

@author: Zibin
'''

from datetime import datetime
from dbReaders.BinReader import BinReader
import pandas as pd
import numpy as np
from math import sqrt
from scipy.stats import skew, kurtosis

''' PartB 2 '''
class TAQStats(object):
    
    def __init__(self, path, ty):
        '''
        Constructor
        '''
        self._path = path
        self._ty = ty

    def sampleLengthDay(self, date):
        # date format is 'YYYYMMDD'
        
        if self._ty == 'trades':
            data = BinReader(self._path, '>QIIf', 100)
        elif self._ty == 'quotes':
            data = BinReader(self._path, '>QIIfIf', 100)
        
        dateStart = datetime.strptime(date, '%Y%m%d') 
        dateEnd = datetime.strptime(str(int(date)+1), '%Y%m%d')
        
        ts = [] # List to store time stampe
        while data.hasNext():
            t = data.next()[0] # Time stamp
            ts.append(t)
        
        for i in range(len(ts)):
            t = datetime.fromtimestamp(ts[i]/1000) # Convert milliseconds to DateTime
            ts[i] = t
        
        sampleLength = 0 # Counter to count the sample
        for time in ts:
            if time > dateStart and time < dateEnd: # Condition to count the number of trades
                sampleLength += 1
            if time > dateEnd: # End loop if the time already passes the target day
                break
            
        data.close()
        return sampleLength
    
    # Part B 2(b)
    def TAQNumber(self):
        
        if self._ty == 'trades':
            data = BinReader(self._path, '>QIIf', 100)
        elif self._ty == 'quotes':
            data = BinReader(self._path, '>QIIfIf', 100)
        
        
        count = 0 
        
        while data.hasNext():
            count += 1 
            data.next()
            
        data.close()
        
        return count
    
    def tradeReturnStat(self):
        
        tradeData = BinReader(self._path, '>QIIf', 100)
        
        day0 = '20070620' # start day
        day1 = '20070621' # one day interval
        dayN = datetime.strptime('20070921', '%Y%m%d')
        oneDay = pd.Timedelta(1, unit="d")
        days = 65 # total number of days
        
        startDate = datetime.strptime(day0, '%Y%m%d')
        endDate = datetime.strptime(day1, '%Y%m%d')
        
        tradeReturn = []
        ts = [] # List to store time stamp
        pr = [] # List to store price
        
        while tradeData.hasNext():
            t, _, _, p = tradeData.next() # Time stamp
            ts.append(t)
            pr.append(p)
        
        for i in range(len(ts)):
            t = datetime.fromtimestamp(ts[i]/1000) # Convert milliseconds to DateTime
            ts[i] = t
        
        tradeData.close()
        
        startIdx = 0 # start index
        endIdx = 0 # end index
        
        for i in range(days):
            startFlag = False
            endFlag = False
            
            # Calculate indexes
            for time in ts:    
                if time > startDate: # start index stops
                    startFlag = True
                if startFlag == False:
                    startIdx += 1
                if time > endDate: # end index stops and exits the loop
                    endFlag = True
                    break
                if endFlag == False:
                    endIdx += 1
            
            prPerChange = (pr[endIdx-1] - pr[startIdx]) / pr[startIdx] # daily return
            if not prPerChange == 0: # No transaction on that day
                tradeReturn.append(prPerChange)
              
            if startDate < dayN: # Move to the next day
                startDate = startDate + oneDay
                endDate = endDate + oneDay
                 
            if startDate.weekday() >= 5: # If the day is Saturday, move it to Monday
                startDate = startDate + oneDay + oneDay
                endDate = endDate + oneDay + oneDay
            
            # Labor day and Independent's day are holidays! 
            if startDate == datetime.strptime('20070903', '%Y%m%d') or startDate == datetime.strptime('20070704', '%Y%m%d'): 
                startDate = startDate + oneDay
                endDate = endDate + oneDay
                
            startIdx = 0
            endIdx = 0
            
            
        # Calculate a bunch of statistics 
        meanReturn = np.mean(tradeReturn)  # Mean
        medianReturn = np.median(tradeReturn) # Median
        stdReturn = np.std(tradeReturn) # Standard deviation
        mad = []
        for i in range(len(tradeReturn)):
            mad.append(abs(tradeReturn[i] - meanReturn))
        MAD = np.median(mad) # Median absolute deviation
        
        annualilzedMeanReturn = (meanReturn + 1) ** 252 - 1 # annualized return, 252 trading days
        annualilzedMedianReturn = (medianReturn + 1) ** 252 - 1
        annualilzedStdReturn = stdReturn * sqrt(252)
        annualizedMAD = (MAD + 1) ** 252 - 1
        skewReturn = skew(tradeReturn) # Skewness
        kurtReturn = kurtosis(tradeReturn) # Kurtosis
        a = sorted(tradeReturn, reverse = True) # Reverse the order, descending
        tenLargest = a[0:10]
        b = sorted(tradeReturn) # ascending
        tenSmallest = b[0:10]
        
        maximums = np.maximum.accumulate(pr)
        drawdowns = 1 - pr / maximums
        maxDrawDown = np.max(drawdowns) # maximum draw down
        
        return annualilzedMeanReturn, annualilzedMedianReturn, annualilzedStdReturn, annualizedMAD, skewReturn, kurtReturn, tenLargest, tenSmallest, maxDrawDown
    
    def midQuoteReturnStat(self):
        quoteData = BinReader(self._path, '>QIIfIf', 100)
                
        day0 = '20070620'
        day1 = '20070621'
        dayN = datetime.strptime('20070921', '%Y%m%d')
        oneDay = pd.Timedelta(1, unit="d")
        days = 65
        
        startDate = datetime.strptime(day0, '%Y%m%d')
        endDate = datetime.strptime(day1, '%Y%m%d')
        
        midReturn = []
        ts = [] # List to store time stamp
        ask = []
        bid = []
        
        while quoteData.hasNext():
            t, _, _, a, _, b = quoteData.next() # Time stamp
            ts.append(t)
            ask.append(a)
            bid.append(b)
        
        for i in range(len(ts)):
            t = datetime.fromtimestamp(ts[i]/1000) # Convert milliseconds to DateTime
            ts[i] = t
        
        quoteData.close()
        
        mid = [] # Mid quote list
        for i in range(len(ask)):
            mid.append((ask[i] + bid[i]) / 2)
        
        startIdx = 0
        endIdx = 0
        
        for i in range(days):
            startFlag = False
            endFlag = False
            
            # 
            for time in ts:    
                if time > startDate:
                    startFlag = True
                if startFlag == False:
                    startIdx += 1
                if time > endDate:
                    endFlag = True
                    break
                if endFlag == False:
                    endIdx += 1
            
            prPerChange = (mid[endIdx-1] - mid[startIdx]) / mid[startIdx]
            if not prPerChange == 0: # No transcation on that day
                midReturn.append(prPerChange)
              
            if startDate < dayN:
                startDate = startDate + oneDay
                endDate = endDate + oneDay
                 
            if startDate.weekday() >= 5: # If the day is Saturday, move it to Monday
                startDate = startDate + oneDay + oneDay
                endDate = endDate + oneDay + oneDay
            
            # Labor day and Independent's day are holidays! 
            if startDate == datetime.strptime('20070903', '%Y%m%d') or startDate == datetime.strptime('20070704', '%Y%m%d'): 
                startDate = startDate + oneDay
                endDate = endDate + oneDay
                
            startIdx = 0
            endIdx = 0
        
        meanReturn = np.mean(midReturn)
        medianReturn = np.median(midReturn)
        stdReturn = np.std(midReturn)
        mad = []
        for i in range(len(midReturn)):
            mad.append(abs(midReturn[i] - meanReturn))
        MAD = np.median(mad)
        
        annualilzedMeanReturn = (meanReturn + 1) ** 252 - 1 # annualized return, 252 trading days
        annualilzedMedianReturn = (medianReturn + 1) ** 252 - 1
        annualilzedStdReturn = stdReturn * sqrt(252)
        annualizedMAD = (MAD + 1) ** 252 - 1 # median absolute deviation
        skewReturn = skew(midReturn)
        kurtReturn = kurtosis(midReturn)
        a = sorted(midReturn, reverse = True) # descending order
        tenLargest = a[0:10]
        b = sorted(midReturn) # ascending order
        tenSmallest = b[0:10]
        
        # calculate maximum drawdown
        maximums = np.maximum.accumulate(mid)
        drawdowns = 1 - mid / maximums
        maxDrawDown = np.max(drawdowns)
        
        return annualilzedMeanReturn, annualilzedMedianReturn, annualilzedStdReturn, annualizedMAD, skewReturn, kurtReturn, tenLargest, tenSmallest, maxDrawDown