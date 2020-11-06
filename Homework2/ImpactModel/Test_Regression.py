'''
Created on Mar 21, 2020

@author: natehuang
'''
import unittest
import csv
import numpy as np
from ImpactModel.Regression import regression
from numpy.testing._private.utils import assert_allclose

class Test(unittest.TestCase):

    def testRegression(self):
        np.random.seed(1)
        # create a fake eta and beta
        x = np.random.rand(2)
        # generate fake data
        with open('test_regression.csv', 'w', newline='\n') as f:
            data_writer = csv.writer(f)
            for i in range(30):
                if i%10 == 0:
                    data_writer.writerow(['Day%i'%(i//9), 
                                          'X[%i]'%(i//9), 
                                          'V[%i]'%(i//9), 
                                          'sigma[%i]'%(i//9), 
                                          'h[%i]'%(i//9)])
                else:
                    generater1 = np.random.rand()
                    generater2 = np.random.rand() + generater1
                    s = np.random.rand()/100 + 0.01
                    # write the fake data into csv
                    data_writer.writerow([None, 1e9*generater1, 1e9*generater2, s, 
                                          regression.impact_cost_fun(x, 1e9*generater1, 1e9*generater2, s, 0)])
                    if i%10==9:
                        data_writer.writerow([None, None, None, None, None])

        reg = regression(filepath = 'test_regression.csv')
        result = reg.compute_eta_beta(regression.impact_cost_fun)[0]
        assert_allclose(result, x, rtol=1e-5)
        
        # Output from assignment2_part1_input
        inputTest = regression(filepath = 'assignment2_part1_input.csv')
        r = inputTest.compute_eta_beta(regression.impact_cost_fun)[0]
        print('Choose day0 = 20070705, day1 = 20070802, day3 = 20070904')
        print('The regression result of assignment2_part1_input is:', r)
        