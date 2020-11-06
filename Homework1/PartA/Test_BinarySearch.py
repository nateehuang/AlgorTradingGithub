'''
Created on Feb 25, 2020

@author: Zibin
'''
import unittest
from PartA.TAQAdjustPlot import binarySearch

'''Test Binary Search Function'''
class Test(unittest.TestCase):


    def test(self):
        a = [1,2,3,6,12,43,67,88] # array
        self.assertTrue(binarySearch(a,0,len(a)-1,12), 4) # check index
        self.assertTrue(binarySearch(a,0,len(a)-1,67), 6) # check index
        self.assertTrue(binarySearch(a,0,len(a)-1,7), -1) # check if not found, return -1


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()