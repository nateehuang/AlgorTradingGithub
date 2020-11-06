'''
Created on Feb 25, 2020

@author: Zibin
'''
import unittest
from dbReaders.TAQQuotesReader import TAQQuotesReader
from PartA.QuoteWriter import QuoteWriter
from dbReaders.BinReader import BinReader


class Test_QuoteWriter(unittest.TestCase):
    
    def test1(self):

        w = QuoteWriter('/Users/Zibin/NYU/qwriter.gz', 1) # Create a .gz file
        
        r = TAQQuotesReader('/Users/Zibin/Documents/R/quotes/20070620/NVDA_quotes.binRQ') # Read a file
        # Using tested readers, test for expected values
        baseTS = r.getSecsFromEpocToMidn() * 1000       
        ts = baseTS + r.getMillisFromMidn(0)
 
        asks = r.getAskSize(0)
        bs = r.getBidSize(0)
        ap = r.getAskPrice(0)
        bp = r.getBidPrice(0)
        
        w.writer(r,1,1) # write to the file
        
        b = BinReader('/Users/Zibin/NYU/qwriter.gz', '>QIIfIf', 100) # use binreader to read
        ts0, _, asksize,askprice,bidsize,bidprice = b.next()
        b.close()
        
        self.assertEquals( ts0, ts ) # Check if time stamps are equal
        self.assertEquals( asksize, asks ) # Check if ask sizes are equal
        self.assertEquals( bidsize, bs ) # Check if bid sizes are equal
        self.assertAlmostEquals( bidprice, bp ) # Check if bid prices are equal
        self.assertAlmostEquals( askprice, ap ) # Check if ask prices are equal


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()