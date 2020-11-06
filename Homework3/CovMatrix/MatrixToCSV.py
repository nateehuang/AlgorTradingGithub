'''
Created on Mar 16, 2020

@author: Zibin
'''

import os
import csv
import holidays
from datetime import timedelta
from datetime import datetime
from LeeCode.BinReader import BinReader
from CovMatrix.DailyData import DailyData
from CovMatrix.MatrixComputer import MatrixComputer
from CovMatrix.Elimination import sliceTS

class MatrixToCSV(object):
    '''
    A class that take a binary trade data file and calculate the lag return
    
    Attributes
    ------
    _dataName : dataName
        Data needed to compute
    
    Method
    ------
    matrixGenerator(self)
        Generate matrix for acquired data
        
    csvGeneratro(self)
        Generate csv file based on the matrix generated
    '''

    def __init__(self, dataName):
        '''
        Constructor
        '''
        
        parentDir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))    
        self._quotePath = parentDir + '/clean_quotes/' 
        self._tradePath = parentDir + '/clean_trades/'
        
        self._dataName = dataName
        self._valMatrix = []
        self._dateList = ['']
        
        startDate = datetime(2007, 6, 20)
        endDate = datetime(2007, 9, 21)        
        usHoliday = holidays.US()
        
        for i in range(int((endDate - startDate).days)):
            nextDate = startDate + timedelta(i)
            if nextDate.weekday() not in (5, 6) and nextDate not in usHoliday:
                tradeDay = nextDate.strftime('%Y%m%d')
                self._dateList.append(tradeDay)
    
          
    def matrixGenerator(self, func):
        '''
        method to generate a matrix for specified data
        
        Parameters
        -----
        func: function
            i.e., lambda x: x.computeMinReturns()
        '''  
           
        for filename in sorted(os.listdir(self._quotePath)): 
            if filename.endswith('.gz'):
                path = self._quotePath + filename
                print('processing '+filename)
                reader = BinReader(path, '>QIIfIf', 100)
                ts = [] # list for time stamp
                si = [] # list for size
                pr = [] # list for price
                while reader.hasNext():
                    d = reader.next()
                    ts.append(d[0])
                    si.append(int((d[2]+d[4])/2)) # mid-quote size
                    pr.append((d[3]+d[5])/2) # mid-quote price
                   
                reader.close()
                          
                sliceIdx = sliceTS(ts) # Slice the time stamp list to get indices for each day
                dailyValue = [filename[:-10]] # the ticker string is the first element 
                
                # For every day of data...   
                for i in range(len(sliceIdx)-1):
                    if i == 64: 
                        # for the last day, increment the last index by 1
                        # to include the last element of each list when instantiating a DailyData object
                        endPoint = sliceIdx[-1]
                        sliceIdx[-1] = endPoint + 1
                    
                    # DailyData object to compute each statistic accordingly
                    data = DailyData(pr, ts, si, sliceIdx[i], sliceIdx[i+1])
                    m = MatrixComputer(data)
                    val = func(m)
                      
                    dailyValue.append(val)                     
                
                self._valMatrix.append(dailyValue) # Add a whole day's computed data to the matrix
        return self._valMatrix
    
    def csvGenerator(self, matrix):   
        '''method to generator a csv based on the matrix given'''  
        
        with open(self._dataName+'.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self._dateList) # date
            writer.writerows(matrix) # data  