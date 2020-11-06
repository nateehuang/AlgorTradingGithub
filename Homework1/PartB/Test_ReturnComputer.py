'''
Created on Feb 25, 2020

@author: natehuang
'''
import os
import gzip
import struct
import unittest
from PartB.ReturnComputer import Computer


class Test_ReturnComputer(unittest.TestCase):
    '''
    classdocs
    '''

    def test(self):
        testPath = os.path.join(os.path.join(os.path.dirname(__file__), os.path.pardir), "Test")
        if not os.path.isdir(testPath):
            os.mkdir(testPath)
        testFile = os.path.join(testPath, "test.gz")
        with gzip.open(testFile, 'wb') as f:
            fmt = '>QIIf'
            content = struct.pack(fmt, 60000, 1, 1, 1.0)
            f.write(content)
            content = struct.pack(fmt, 60000, 1, 1, 1.0)
            f.write(content)
            content = struct.pack(fmt, 120000, 1, 1, 1.5)
            f.write(content)
            content = struct.pack(fmt, 180000, 1, 1, 3.0)
            f.write(content)
            content = struct.pack(fmt, 239000, 1, 1, 6.0)
            f.write(content)
            content = struct.pack(fmt, 241000, 1, 1, 9.0)
            f.write(content)
        
        tr = Computer(testFile, ty="trades")
        ls = tr.computeReturn(1)
        self.assertAlmostEqual(len(ls), 3)
        # the first 1 second lag return is 1.5/1-1 = 0.5
        self.assertAlmostEqual(ls[0], 0.5)
        # the second 1 second lag return is 3/1.5-1 = 1
        self.assertAlmostEqual(ls[1], 1)
        # the second 1 second lag return is 6/3-1 = 1
        self.assertAlmostEqual(ls[2], 1)
        
        ls = tr.computeReturn(2)
        
        self.assertAlmostEqual(len(ls), 1)
        # the first 2 seconds lag return is 3/1-1 = 2
        self.assertAlmostEqual(ls[0], 2)
        
        # test quote 
        with gzip.open(testFile, 'wb') as f:
            fmt = '>QIIfIf'
            content = struct.pack(fmt, 60000, 1, 1, 1.0, 1, 1.0)
            f.write(content)
            content = struct.pack(fmt, 60000, 1, 1, 1.0, 1, 1.0)
            f.write(content)
            content = struct.pack(fmt, 120000, 1, 1, 1, 1, 2.0)
            f.write(content)
            content = struct.pack(fmt, 180000, 1, 1, 2.0, 1, 4.0)
            f.write(content)
            content = struct.pack(fmt, 239000, 1, 1, 1.0, 1, 11.0)
            f.write(content)
            content = struct.pack(fmt, 241000, 1, 1, 9.0, 1, 9.0)
            f.write(content)
        
        tr = Computer(testFile, ty="quotes")
        ls = tr.computeReturn(1)
        self.assertAlmostEqual(len(ls), 3)
        # the first 1 second lag return is 1.5/1-1 = 0.5
        self.assertAlmostEqual(ls[0], 0.5)
        # the second 1 second lag return is 3/1.5-1 = 1
        self.assertAlmostEqual(ls[1], 1)
        # the second 1 second lag return is 6/3-1 = 1
        self.assertAlmostEqual(ls[2], 1)
        
        ls = tr.computeReturn(2)
        
        self.assertAlmostEqual(len(ls), 1)
        # the first 2 seconds lag return is 3/1-1 = 2
        self.assertAlmostEqual(ls[0], 2)
        
        