'''
Created on Feb 24, 2020

@author: natehuang
'''
import os
from dbReaders.BinReader import BinReader

class TradeReturn(object):
    '''
    A class that take a binary trade data file and calculate the lag return
    
    Attributes
    ------
    _Path : str
        Path to the directory of the data read
    
    Method
    ------
    GetReturn(tick, lagT)
        Get lagT lag return on tick
    '''


    def __init__(self, Path):
        '''
        Parameters
        ------
        Path : str
            The path to the directory which contains the binary trade data files
        '''
        self._Path = Path
        
    def GetReturn(self, tick, lagT):
        '''
        Get the lag return of a particular ticker trades 
        
        Parameters
        ------
        tick : str
            The ticker we want to compute the return from
            
        lagT : int
            The lag, in millisecond, we want to use to compute lag return 
        '''
        # read the trade file
        self._tReader = BinReader(os.path.join(self._Path, tick+"_trades.gz"), 
                                  '>QIIf', 100)
        
        # eight hour in milisecond
        eighthour = int(2.88e7)
        
        r_lag = []
        # the next time we are looking for in the list
        find_t = self._tReader.getSN() + lagT
        # setup
        now = self._tReader.next()
        # the previous time we have observed
        pre_t = now[0]
        # the previous price we have observed
        pre_p = now[3]
        # the base price we use the calculate the return
        base_p = now[3]
        # a time stamp to check if we go to tomorrow data
        today = now[0]
        
        # loop through the data 
        while self._tReader.hasNext():
            now = self._tReader.next()
            # get the current time stamp
            t = now[0]
            
            if t > today + eighthour:
                # if the current time is after the market time, 
                # go to tomorrow and start again
                today = t
                base_p = now[3]
                
            elif t > find_t:
                # if the current time is greater than the time,
                # use the previous price to calculate the lag return 
                r_lag.append(pre_p/base_p - 1)
                base_p = pre_p
                # the next time we are looking for 
                find_t = pre_t + lagT
            elif t == find_t:
                # if the current time is exactly the time we are looking for,
                # calculate the return 
                r_lag.append(now[3]/base_p - 1)
                base_p = now[3]
                find_t += lagT
            pre_p = now[3]
            pre_t = now[0]
            
        return r_lag