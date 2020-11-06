'''
Created on Mar 21, 2020

@author: Zibin
'''
import unittest
from ImpactModel.DailyData import DailyData
from ImpactModel.MatrixComputer import MatrixComputer
from LeeCode.TickTest import TickTest
import numpy as np

class Test(unittest.TestCase):
    '''
    Test all functions in Matrix Computer class
    '''
    
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName=methodName)
    
        self._ts = [1183642200000]
        oneMin = 60 * 1000
        
        for i in range(9):
            self._ts.append(self._ts[i] + oneMin) # add one minute to each element
            
        self._ts.append(1183664100000) # 15:35:00
        self._ts.append(1183664100000 + oneMin) # 15:36:00
    
        self._si = [100,200,250,250,100,600,500,400,200,300,100,150] # size list
        self._pr = [2.5, 2.0, 2.5, 3.0, 3.5, 2.5, 2.0, 1.5, 2.0, 1.5, 1.0, 1.5] # price list
        self._d = DailyData(self._pr,self._ts,self._si,0,12)
        self._m = MatrixComputer(self._d)
    
    def testTerminalPrice(self):
        ter = self._m.computeTerminalPrice()
        ans = (1.5+2+1.5+1+1.5) / 5 # Average of last five prices
        self.assertAlmostEqual(ter, ans)
        
    def testArrivalPrice(self):
        arr = self._m.computeArrivalPrice()
        ans = (2.5+2.0+2.5+3.0+3.5) / 5 # Average of first five prices
        self.assertAlmostEqual(arr, ans)
        
    def testDailyVolume(self):
        vol = self._m.computeTotalDailyVolume()
        ans = sum(self._si) # Sum of number of shares
        self.assertTrue(vol == ans)
        
    def testVWAP400(self):
        # (price * corresponding number of shares) / total number of shares
        # Use all data
        ans = 0
        for i in range(len(self._si)):
            ans += (self._pr[i] * self._si[i])
        ans /= self._m.computeTotalDailyVolume()
        
        vwap400 = self._m.computeVWAP400()
        self.assertAlmostEqual(vwap400, ans)
        
    def testVWAP330(self):
        # Remove the last two elements since they are after 15:30
        ans = 0
        for i in range(len(self._si)-2):
            ans += (self._pr[i] * self._si[i])
        ans = ans / (self._m.computeTotalDailyVolume() - 100 - 150)
        
        vwap330 = self._m.computeVWAP330()
        self.assertAlmostEqual(vwap330, ans)
        
    def testImbalance(self):
        # imbalance from 9:30 to 15:30
        # Remove the last two elements since they are after 15:30
        tt = TickTest()
        
        # Classify trade 
        tickResult = np.array(tt.classifyAll(self._d, self._ts[0], self._ts[-3] + 1000))  
        tick = tickResult.T[2]        
        size = tickResult.T[3]
        shares = np.sum(np.multiply(tick, size))
        
        vwap = self._m.computeVWAP330()
        ans = shares * vwap
        im = self._m.computeImbalance()
        self.assertAlmostEqual(im, ans)
        
    def testTwoMinReturn(self):
        # The first 5 elements are within 2 mins
        # The next 2 elements are within the next 2 mins
        self._ts = [1183642200000, 1183642230000, 1183642260000, 1183642290000, 1183642320000, 1183642360000, \
                    1183642390000, 1183642450000]
        self._pr = [1,2,3,1.5,1.5,3,2,3]
        self._si = [100,200,300,200,300,100,200,300]
        self._d = DailyData(self._pr,self._ts,self._si,0,12)
        self._m = MatrixComputer(self._d)

        first = 1.5/1 - 1 # First two minute returns
        second = 2/3 - 1 # Second two minute returns
        
        ans = self._m.computeTwoMinReturns() # a list
        
        self.assertAlmostEqual(first, ans[0])
        self.assertAlmostEqual(second, ans[1])
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testTerminalPrice']
    unittest.main()