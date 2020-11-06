'''
Created on Mar 21, 2020

@author: Zibin
'''
import unittest
from ImpactModel.Elimination import dateTrade
from ImpactModel.Elimination import sliceTS


class Test(unittest.TestCase):

    def testDateTrade(self):
        myList = dateTrade()
        indepDay = '20070704'
        laborDay = '20070903'
        weekDay = '20070703'
        weekend = '20070623'
        self.assertTrue(indepDay not in myList) # independent day should not be in the list
        self.assertTrue(laborDay not in myList) # labor day should not be in the list
        self.assertTrue(weekend not in myList) # weekend should not be in the list
        self.assertTrue(weekDay in myList) # week day should be in the list
        self.assertEquals(len(myList), 65)
    
    def testSliceTS(self):
        # 1183642200000: 20070705 9:30:00
        # 1183642201000: 20070705 9:30:01
        # 1183642230000: 20070705 10:20:30
        # 1183728600000: 20070706 9:30:00
        # 1183748700000: 20070706 15:05:00
        # 1183815000000: 20070707 9:30:00
        # 1183815100000: 20070707 9:31:40
        ts = [1183642200000, 1183642201000, 1183645230000, 1183728600000, 1183748700000, 1183815000000, 1183815100000]
        myIdx = sliceTS(ts)
        self.assertTrue(myIdx[0] == 0) # start of 20070705
        self.assertTrue(myIdx[1] == 3) # start of 20070706
        self.assertTrue(myIdx[2] == 5) # start of 20070707
        self.assertTrue(myIdx[3] == 6) # last element of ts list

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDateTrade']
    unittest.main()