'''
Created on Feb 23, 2020

@author: furonghuang
'''
import struct
import gzip
class QuoteWriter(object):
    '''
    classdocs
    '''


    def __init__(self, filePath, tickerID):
        '''
        Constructor
        '''
        self._filePath = filePath
        self._tickerId = tickerID
        
    def writer(self, quote, priceFact=1, shareFact = 1):
        s = struct.Struct( ">QIIfIf" ) 
        out = gzip.open( self._filePath, "ab" )
        baseTS = quote.getSecsFromEpocToMidn() * 1000
        for i in range( quote.getN() ):
            ts = baseTS + quote.getMillisFromMidn( i )
            out.write( s.pack( ts, self._tickerId, 
                               int(quote.getAskSize(i)*shareFact), 
                               quote.getAskPrice(i)/priceFact, 
                               int(quote.getBidSize(i)*shareFact),
                               quote.getBidPrice(i)/priceFact) )
        out.close()
        