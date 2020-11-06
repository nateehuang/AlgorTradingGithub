import unittest
from dbReaders.TAQTradesReader import TAQTradesReader
from PartA.TradeWriter import TradeWriter
from dbReaders.BinReader import BinReader

class Test_TradeWriter(unittest.TestCase):
    
    def test1(self):
        
        dirc = '/Users/Zibin/NYU/twriter.gz'

        w = TradeWriter(dirc, 1) # Create a .gz file on directory
        
        r = TAQTradesReader('/Users/Zibin/Documents/R/trades/20070620/NVDA_trades.binRT') # Read a file
        # Using tested readers, test for expected values
        baseTS = r.getSecsFromEpocToMidn() * 1000       
        ts = baseTS + r.getMillisFromMidn(0)
 
        s = r.getSize(0) 
        p = r.getPrice(0)
        
        w.writer(r,1,1) # write to the file
        
        b = BinReader(dirc, '>QIIf', 100) # use binreader to read
        ts0, _, size0, p0 = b.next()
        b.close()
        
        self.assertEquals( ts0, ts ) # Check if time stamps are equal
        self.assertEquals( size0, s ) # Check if numbers of shares are equal
        self.assertAlmostEquals( p0, p ) # Check if prices are equal

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()