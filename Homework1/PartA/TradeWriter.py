'''
Created on Feb 23, 2020

@author: furonghuang
'''
import struct
import gzip
class TradeWriter(object):
    '''
    classdocs
    '''

    def __init__(self, filePath, tickerID):
        '''
        Constructor
        '''
        self._filePath = filePath
        self._tickerId = tickerID
        
        
    def writer(self, trade, priceFact=1, shareFact = 1):
        s = struct.Struct( ">QIIf" ) 
        out = gzip.open( self._filePath, "ab" )
        baseTS = trade.getSecsFromEpocToMidn() * 1000
        for i in range( trade.getN() ):
            ts = baseTS + trade.getMillisFromMidn( i )
            out.write( s.pack( ts, 
                               self._tickerId, 
                               int(trade.getSize(i)*shareFact), 
                               trade.getPrice(i)/priceFact ) )
        out.close()
        