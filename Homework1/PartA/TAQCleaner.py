'''
Created on Feb 23, 2020
@author: Nate, Zibin, Martin
'''

import os
import gzip
import struct
import numpy as np
from dbReaders.BinReader import BinReader
from PartA.CircularArray import CircularArray

class CleanTAQ(object):
    '''
    A class that clean the adjusted TAQ data
    '''


    def __init__(self, fileDirectory, k = 5, gCoeff=0.0005):
        '''
        Parameters
        ------
        fileDirectory : str
            Path to the sources of the adjusted TAQ data
        
        k : int
            Windows parameter for filtering model
            
        gCoeff : float
            Gamma coefficient parameter for the filtering model
            
        '''
        self._k = k
        self._gCoeff = gCoeff
        self._source = fileDirectory

        # set the save directory
        self._direct = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        self._tradeSaveDirect = os.path.join(self._direct, "clean_trades")
        self._quoteSaveDirect = os.path.join(self._direct, "clean_quotes")
        # if the directories does not exist, create
        if not os.path.isdir(self._tradeSaveDirect):
            os.mkdir(self._tradeSaveDirect)
        if not os.path.isdir(self._quoteSaveDirect):
            os.mkdir(self._quoteSaveDirect)
        
    
    def threshold(self, p, mean, std, tot_mean):
        '''
        Determine if the data stay or being remove
        
        Parameters
        ------
        p : float
            current data price
            
        mean : float
            current window mean
            
        std : float
            current window std
            
        tot_mean : float 
            mean of all of the data
            
        Returns
        ------
          : boolean
              True if the data stays, False if the data goes
        '''
        upperbound = 2* std + self._gCoeff*tot_mean

        if np.abs(p-mean)<upperbound:
            return True
        else:
            return False
        
    def writer(self, fmt):
        s = struct.Struct( fmt ) 
        return s
  
        
    def clean_trades(self, tick, subset=False, save = False):
        '''
        Clean the TAQ trades data
        
        Parameters
        ------
        tick : str
            The ticker of the data to be cleaned
            
        subset : boolean
            If True, only clean a subset of the data
        
        save : boolean
            If True, save the data into binary files to the certain directory
            
        Returns
        ------
        A tuple of number of the data, time stamp, clean price
        '''
        # return a tuple of lists of clean trades data
        # if parameter save = True, save the data into file
        print("Cleaning trade", tick)
        # set up the writer format
        self._tReader = BinReader(os.path.join(self._source, tick+"_trades.gz"), 
                                  '>QIIf', 100)
        prices = CircularArray(self._k)
        
        if save:
            # set up the writer
            tw = self.writer('>QIIf')
            out = gzip.open( os.path.join(self._tradeSaveDirect, tick+"_trades.gz"), "ab")
        else:
            clTs = []
            clIds = []
            clSs = []
            clPs = []
        
        ts = []
        ids = []
        ss = []
        ps = []
        
        count = 0
        # get the data into lists
        while self._tReader.hasNext():
            t, i, s, p = self._tReader.next()
            ts.append(t)
            ids.append(i)
            ss.append(s)
            ps.append(p)
            count += 1
        print(tick, "has ", count, "entries")
        
        # subset the data
        if subset:
            stop = int(count/65)
        else:
            stop = count
        tot_mean = np.mean(ps)
        
        screen_tracker = 0
        threshold_tracker = 0
        
        # initialize the filter  
        while threshold_tracker < self._k:
            prices.add(ps[threshold_tracker])
            threshold_tracker += 1

        # get the current mean in the window
        pm = prices.mean()
        # get the std in the window
        std = prices.std()
        
        # screen the first k/2 data
        while screen_tracker < int(self._k/2) + 1:
            cp = ps[screen_tracker]
            # if threshold return True, keep the data
            # otherwise don't take the data
            if self.threshold(cp, pm, std, tot_mean):
                if save:
                    out.write(tw.pack(ts[screen_tracker], 
                                  ids[screen_tracker], 
                                  ss[screen_tracker], 
                                  ps[screen_tracker]))
                else:
                    clTs.append(ts[screen_tracker])
                    clIds.append(ids[screen_tracker])
                    clSs.append(ss[screen_tracker])
                    clPs.append(ps[screen_tracker])

            screen_tracker += 1
        
        # screen the rest of the data
        while screen_tracker < stop:
            
            cp = ps[screen_tracker]
            
            if threshold_tracker < count:
                prices.add(cp)

                pm = prices.mean()
                std = prices.std()
                
            if self.threshold(cp, pm, std, tot_mean):
                if save:
                    out.write(tw.pack(ts[screen_tracker], 
                                ids[screen_tracker], 
                                ss[screen_tracker], 
                                ps[screen_tracker]))
                else:
                    clTs.append(ts[screen_tracker])
                    clIds.append(ids[screen_tracker])
                    clSs.append(ss[screen_tracker])
                    clPs.append(ps[screen_tracker])
                    
            screen_tracker += 1
            threshold_tracker += 1
            
        if save:
            out.close()
        else:
            return (count, clTs, clPs)
            
            
    def clean_quotes(self, tick, subset=False, save=False):
        print("Cleaning quote ", tick)
        self._qReader = BinReader(os.path.join(self._source, tick+"_quotes.gz"), 
                                  '>QIIfIf', 100)
        mPrices = CircularArray(self._k)
        if save:
            qw = self.writer('>QIIfIf')
            out = gzip.open( os.path.join(self._quoteSaveDirect, tick+"_quotes.gz"), "ab" )
        else:
            clTs = []
            clIds = []
            clAss = []
            clAps = []
            clBss = []
            clBps = []
            
        
        ts = []
        ids = []
        ass = []
        aps = []
        bss = []
        bps = []
        count = 0
        while self._qReader.hasNext():
            t, i, asi, ap, bs, bp = self._qReader.next()
            ts.append(t)
            ids.append(i)
            ass.append(asi)
            aps.append(ap)
            bss.append(bs)
            bps.append(bp)
            count += 1
        print(tick, "has ", count, "entries")
        if subset:
            stop = int(count/65)
        else:
            stop = count
            
        amean = np.mean(aps)
        bmean = np.mean(bps)
        mid_mean = (amean + bmean)/2
        
        
        screen_tracker = 0
        threshold_tracker = 0
        while threshold_tracker < self._k:
            mPrices.add((aps[threshold_tracker]+bps[threshold_tracker])/2)
            threshold_tracker += 1

        mpm = mPrices.mean()
        mstd = mPrices.std()
        
        while screen_tracker < int(self._k/2) + 1:
            mcp = (aps[screen_tracker] + bps[screen_tracker])/2
            if self.threshold(mcp, mpm, mstd, mid_mean):
                if save:
                    out.write(qw.pack(ts[screen_tracker], 
                                      ids[screen_tracker],
                                      ass[screen_tracker],
                                      aps[screen_tracker], 
                                      bss[screen_tracker], 
                                      bps[screen_tracker]))
                else:
                    clTs.append(ts[screen_tracker])
                    clIds.append(ids[screen_tracker])
                    clAss.append(ass[screen_tracker])
                    clAps.append(aps[screen_tracker])
                    clBss.append(bss[screen_tracker])
                    clBps.append(bps[screen_tracker])
            screen_tracker += 1

        while screen_tracker < stop:
            mcp = (aps[screen_tracker] + bps[screen_tracker])/2

            if threshold_tracker < count:
                mPrices.add(mcp)
                mpm = mPrices.mean()
                mstd = mPrices.std()
                threshold_tracker += 1
            if self.threshold(mcp, mpm, mstd, mid_mean):
                if save:
                    out.write(qw.pack(ts[screen_tracker], 
                                      ids[screen_tracker], 
                                      ass[screen_tracker],
                                      aps[screen_tracker],                                      
                                      bss[screen_tracker], 
                                      bps[screen_tracker]))
                else:
                    clTs.append(ts[screen_tracker])
                    clIds.append(ids[screen_tracker])
                    clAss.append(ass[screen_tracker])
                    clAps.append(aps[screen_tracker])
                    clBss.append(bss[screen_tracker])
                    clBps.append(bps[screen_tracker])
            
            screen_tracker += 1
            
        if save:
            out.close()
        else:
            return (count, clTs, clAps, clBps)