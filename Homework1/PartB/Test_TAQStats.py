'''
Created on Feb 25, 2020

@author: Zibin
'''
import os
import unittest
from PartB.TAQStats import TAQStats

''' 
This class test the statistics computed in TAQStat class
Since the function written TAQStat is highly specialized for the data
We can only use the real data to test
'''

class Test(unittest.TestCase):

    def test(self):
        print('Complete the test requires a few minutes')
        parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
        path = parentddir + '/PartA/adjusted_trades/KSS_trades.gz'

        stat = TAQStats(path, 'trades')
        
        self.assertAlmostEqual(stat.tradeReturnStat()[0], -0.55717147) # mean
        self.assertAlmostEqual(stat.tradeReturnStat()[1], -0.68048294) # median
        self.assertAlmostEqual(stat.tradeReturnStat()[2], 0.349296851) # standard deviation
        self.assertAlmostEqual(stat.tradeReturnStat()[3], 21.69121743) # mad
        self.assertAlmostEqual(stat.tradeReturnStat()[4], 0.762531473) # skewness
        self.assertAlmostEqual(stat.tradeReturnStat()[5], 0.874094844) # kurtosis
        self.assertAlmostEqual(stat.tradeReturnStat()[8], 0.274661481) # max drawdown
        
        parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
        path = parentddir + '/clean_trades/KSS_trades.gz'

        stat2 = TAQStats(path, 'trades')
        self.assertAlmostEqual(stat2.tradeReturnStat()[0], -0.568795852676113) # mean
        self.assertAlmostEqual(stat2.tradeReturnStat()[1], -0.728641720680403) # median
        self.assertAlmostEqual(stat2.tradeReturnStat()[2], 0.3471293807174141) # standard deviation
        self.assertAlmostEqual(stat2.tradeReturnStat()[3], 17.629234897105075) # mad
        self.assertAlmostEqual(stat2.tradeReturnStat()[4], 0.7821153292052) # skewness
        self.assertAlmostEqual(stat2.tradeReturnStat()[5], 0.9212095595774854) # kurtosis
        self.assertAlmostEqual(stat2.tradeReturnStat()[8], 0.2723127912738612) # max drawdown
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()