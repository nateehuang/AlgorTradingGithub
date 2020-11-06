from LeeCode.FirstPriceBuckets import FirstPriceBuckets
from LeeCode.LastPriceBuckets import LastPriceBuckets

class ReturnBuckets(object):
    '''
    This class will be used to build return buckets, eg 2 minute returns
    '''
    
    def __init__(
        self, 
        data, # An object that implements getTimestamp(i), getPrice(i), getN() 
        startTS, # In milliseconds from midnight
        endTS, # In milliseconds from midnight
        numBuckets # Desired number of return buckets
    ):
        '''
        Builds return buckets for above specified time intervals
        '''
        # Make sure data is in the right format
        if ( data == None ) or ( data.getPrice == None ) or ( data.getTimestamp == None ) or ( data.getN == None ):
            raise Exception( "Your data object must implement getPrice(i), getTimestamp(i), and getN() methods" ) 
        
        # Save start and end times
        if startTS == None:
            startTS = 19 * 60 * 60 * 1000 / 2
        if endTS == None:
            endTS = 16 * 60 * 60 * 1000
        self._startTS = startTS
        self._endTS = endTS
        
        self._startTimestamps = [None]*numBuckets
        self._endTimestamps = [None]*numBuckets
        self._returns = [None]*numBuckets
        
        firstPriceBuckets = FirstPriceBuckets( data, numBuckets, self._startTS, self._endTS )
        lastPriceBuckets = LastPriceBuckets( data, numBuckets, self._startTS, self._endTS )
        for i in range( 0, firstPriceBuckets.getN() ):
            startTimestamp = firstPriceBuckets.getTimestamp( i )
            endTimestamp = lastPriceBuckets.getTimestamp( i )
            startPrice = firstPriceBuckets.getPrice( i )
            endPrice = lastPriceBuckets.getPrice( i )
            if startTimestamp == None or endTimestamp == None:
                continue
            self._startTimestamps[ i ] = startTimestamp
            self._endTimestamps[ i ] = endTimestamp
            self._returns[ i ] = ( endPrice / startPrice ) - 1.0
    
    def getStartTimestamp(self, index ):
        return self._startTimestamps[ index ]                

    def getEndTimestamp(self, index ):
        return self._endTimestamps[ index ]
    
    def getReturn(self, index ):
        return self._returns[ index ]
    
    def getN(self):
        return len( self._startTimestamps )     
    
    def getReturns(self):
        return self._returns        