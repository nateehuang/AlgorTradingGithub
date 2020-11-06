'''
Created on Mar 21, 2020

@author: Zibin
'''
import unittest
from ImpactModel.DailyData import DailyData

class Test(unittest.TestCase):
    '''
    Test the DailyData class
    '''
    
    def testDailyData(self):
        ts = [1183642200000, 1183642201000, 1183645230000, 1183728600000, 1183748700000, 1183815000000, 1183815100000]
        si = [100,200,250,220,320,600,500]
        pr = [2.5, 2.6, 2.8, 19.6, 19.4, 30.5, 30.7]
        
        d = DailyData(pr,ts,si,0,3) # instantiate an object (20070705)
        
        # check get price/size/timestamp functions
        self.assertTrue(d.getPrice(1) == 2.6)
        self.assertTrue(d.getPrice(2) == 2.8)
        self.assertTrue(d.getTimestamp(1) == 1183642201000)
        self.assertTrue(d.getSize(1) == 200)
        
        price = d.getPrices() # price list
        self.assertTrue(price[0] == 2.5)
        self.assertTrue(price[1] == 2.6)
        self.assertTrue(price[2] == 2.8)
        
        size = d.getSizes() # size list
        self.assertTrue(size[0] == 100)
        self.assertTrue(size[1] == 200)
        self.assertTrue(size[2] == 250)
        
        timestamp = d.getTimestamps() # timestamp list
        self.assertTrue(timestamp[0] == 1183642200000)
        self.assertTrue(timestamp[1] == 1183642201000)
        self.assertTrue(timestamp[2] == 1183645230000)
                
        self.assertTrue(d.getN() == 3) # The length is 3
        self.assertTrue(d.getNumShares() == 100+200+250) # sum of share traded

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDailyData']
    unittest.main()