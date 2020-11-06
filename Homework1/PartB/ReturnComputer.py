'''
Created on Feb 25, 2020

@author: Nate, Zibin, Martin
'''
from dbReaders.BinReader import BinReader

class Computer(object):
    '''
    A class to compute X-minute returns of trades and mid-quotes
    
    Attributes
    ------
    _ts : list
        A list of time stamps from the data
        
    _pr : list 
        A list of prices from the data
        
    Methods
    ------
    computeReturn(x)
        Return the X-time lag return of the trade price/mid quote price for trade/quote data
    '''

    def __init__(self, filePath, ty):
        '''
        Parameters
        ------
        filePath : str
            The file path of the data
            
        ty : str
            type of the data, either 'trades' or 'quotes'
        '''
        
        # Read the data in
        if ty == "trades":
            reader = BinReader(filePath, '>QIIf', 100)
            self._ts = []
            self._pr = []
            while reader.hasNext():
                now = reader.next()
                self._ts.append(now[0])
                self._pr.append(now[3])
            
            
        elif ty == "quotes":
            reader = BinReader(filePath, '>QIIfIf', 100)
            self._ts = []
            self._pr = []
            while reader.hasNext():
                now = reader.next()
                self._ts.append(now[0])
                self._pr.append((now[3]+now[5])/2)
                
        
        
    def computeReturn(self, x):
        '''
        Compute the X-minute return
        
        Parameters
        ------
        x : int
            Minute
        '''
        # Convert minute to millisecond
        xInMiliSec = 60 * 1000 * x
        r = []
        # find the next time (after X minute)
        find_t = self._ts[0] + xInMiliSec
        # record the previous time and price
        pre_t = find_t
        pre_p = self._pr[0]
        # record the base time and price for return calculation
        base_t = self._ts[0]
        base_p = self._pr[0]
        
        for i, p in enumerate(self._pr):
            # if the time has passed
            if self._ts[i] > find_t:
                if base_t == pre_t:
                # if the previous time is the same as base time,
                # move to find the next time
                    find_t = self._ts[i] + xInMiliSec
                else:
                # use the previous price to calculate return
                    r.append(pre_p/base_p-1)
                    find_t += xInMiliSec
                base_t = self._ts[i]
                base_p = p
            # if the time has been found
            # calculate the return then move on
            elif self._ts[i] == find_t:
                r.append(p/base_p-1)
                base_p = p
                find_t += xInMiliSec
            pre_t = self._ts
            pre_p = p
                
        return r
        