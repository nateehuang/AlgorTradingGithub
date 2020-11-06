'''
Created on Feb 23, 2020

@author: furonghuang
'''
import unittest
import numpy as np
from PartA.CircularArray import CircularArray

class Test_CircularArray(unittest.TestCase):
    '''
    classdocs
    '''
    
    def test(self):
        ca = CircularArray(5)
        for i in range(5):
            ca.add(i)
            
        for i in range(5):
            self.assertTrue(ca.get(i) == i)
        
        ca.add(5)
        self.assertTrue(ca.get(0)==5)
        ca.add(6)
        self.assertTrue(ca.get(1)==6)
        ca.add(7)
        self.assertTrue(ca.get(2)==7)
        ca.add(8)
        self.assertTrue(ca.get(3)==8)
        ca.add(9)
        self.assertTrue(ca.get(4)==9)
        
        self.assertAlmostEqual(ca.mean(), 7)
        
        self.assertAlmostEqual(ca.std(), np.sqrt(10)/2)