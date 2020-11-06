'''
Created on Apr 12, 2020

@author: guanyuyao
'''

import unittest
import HW3_part2.OptTcost as opt
import pandas as pd
import numpy as np
import xlwings

class Test(unittest.TestCase):

    def test_constructor(self):
        '''
        tests the constructor of Opt_Tcost class
        '''
        
        w0 = np.array([1,1,1])
        W = 10
        mu = np.array([0.3,0.4,-0.5])
        cov = np.array([[0.000474, 3.55e-05, 4.44e-05],[3.55e-05, 0.000645, 1.44e-05],[4.44e-05, 1.44e-05, 0.000264]])
        lam1 = 1
        lam2 = 1
        gamma = 0.3
        eta = 0.2
        V = np.array([5,5,5])
        Theta = np.array([3,3,3])
        T = 1
        p = np.array([0.1,0.3,0.2])
        
        optimizer = opt.OptTcost(w0, W, mu, cov, lam1, lam2, gamma, eta, V, Theta, T, p)
        optimizer.solve()
        
    def test_Excel(self):
        '''
        read the parameter input in excel and write the result to the file
        '''
        
        # read the data on sheet 1 and 3
        sheet1 = pd.read_excel('assignment3_part2_input.xlsx', sheet_name='model params', header=0, usecols = "A,C,D:F")
        sheet2 = pd.read_excel('assignment3_part2_input.xlsx', sheet_name='covariance matrix (500X500)', index_col=0, header=0)
        sheet3 = pd.read_excel('assignment3_part2_input.xlsx', sheet_name='constraint', header=0, usecols = "D")
        
        # read ticker list
        tickers = sheet2.index.to_numpy()
        
        # read covariance matrix
        cov = sheet2.to_numpy()
        
        # read mean vector
        mu = sheet1['u'].values
        
        # read eta
        eta = sheet1['eta'].values[0]
        
        # read lambda 
        lam1 = sheet1['lambda'].values[0]
        
        # read gamma (call it lambda2)
        lam2 = sheet1['gamma'].values[0]
        
        # read w0
        w0 = sheet1['w_0 (initial)'].values
        
        # read W
        W = sheet3['W'].values[0]
        
        # use gamma(in TC) as it is in the paper of Almgren
        gamma = 0.314
        
        # choose daily values
        T = 1
        
        # pick a trading day and read V
        date = '20070628'
        
        V = pd.read_csv("imbalance.csv", header=0, index_col = 0)[date][tickers].values
        
        # read Theta
        
        sheet4 = pd.read_excel("s_p500.xlsx", dtype=str).dropna(subset=['Ticker Symbol', 'Names Date', 'Price or Bid/Ask Average', 'Shares Outstanding'])
        sheet4 = sheet4[['Names Date','Ticker Symbol','Price or Bid/Ask Average', 'Shares Outstanding']]
        sheet4['Price or Bid/Ask Average'] = pd.to_numeric(sheet4['Price or Bid/Ask Average'], errors='coerce').fillna(0.)
        sheet4['Shares Outstanding'] = pd.to_numeric(sheet4['Shares Outstanding'], errors='coerce').fillna(0)

        shares = sheet4[sheet4['Names Date'] == date]
        shares = shares.set_index('Ticker Symbol').loc[list(tickers)]
        shares = shares[~shares.index.duplicated(keep='first')]
        
        Theta = shares['Shares Outstanding'].values
        
        # read mid-quote price
        
        p = shares['Price or Bid/Ask Average'].values
        
        # do optimization----------------------------------------------------------------------
        
        optimizer = opt.OptTcost(w0, W, mu, cov, lam1, lam2, gamma, eta, V, Theta, T, p)
        sol_opt = np.array(optimizer.solve())
        sol_opt1 = sol_opt.reshape((len(w0),)) # change solution to numpy array for later calculation
        
        # calculate permanent and temporary impact of the optimal solution
        impact_perm = []
        impact_temp = []
        
        for i in range(len(sol_opt1)):
            
            tc = optimizer.TC(sol_opt1[i] - w0[0], gamma, np.sqrt(cov[i][i]), V[i], Theta[i], eta, T, p[i]) 
            impact_perm.append(tc[0])
            impact_temp.append(tc[1])
        
        impact_perm = np.array(impact_perm)
        impact_temp = np.array(impact_temp)
        
        impactTT_perm = np.sum(impact_perm)      # total permanent impact
        impactTT_temp = np.sum(impact_temp)      # total temporary impact
        impactTT = impactTT_perm + impactTT_temp # total impact
        
        # write the solutions to the existing excel file----------------------------------------------
        wb = xlwings.Book("assignment3_part2_input.xlsx")  
        
        Sheet1 = wb.sheets[0]
        Sheet2 = wb.sheets[2]
        
        #update w_optimal
        Sheet1.range('B2:B489').value = sol_opt
        
        #update permanent impact (for TC)
        Sheet1.range('H2:H489').value = impact_perm.reshape((len(impact_perm),1))
        
        #update TC(delta_w)
        Sheet2.range('A2').value = impactTT
        
        #update temporary TC(delta_w)
        Sheet2.range('B2').value = impactTT_temp
        
        #update permanent TC(delta_w)
        Sheet2.range('C2').value = impactTT_perm
        
        wb.save()
        wb.close()
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()