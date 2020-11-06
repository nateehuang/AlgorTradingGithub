'''
Created on Apr 6, 2020

@author: huang
'''
import numpy as np
import pandas as pd
from CovMatrix.MatrixToCSV import MatrixToCSV
from CovMatrix.Covariance import Covariance

if __name__ == '__main__':
    np.random.seed(1)
    
    # below codes compute the five minutes return from raw quotes data and save it as csv in local
#     mc = MatrixToCSV("fiveMinReturns")
#     mc.csvGenerator(mc.matrixGenerator(lambda x: x.computeMinReturns()))
    
    # below codes read five minutes return csv generated above and out put table A as csv in local
    cov = Covariance(path="fiveMinReturns.csv")
    cov.output_table_A()