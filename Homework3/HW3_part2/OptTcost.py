'''
Created on Apr 12, 2020

@author: guanyuyao
'''

import numpy as np
from cvxopt import solvers, matrix
from scipy.sparse import spdiags

class OptTcost(object):
    '''
    class used to perform non-linear optimization on the second specified portfolio problem
    '''
    
    def __init__(self, w0, W, mu, Sig, lam1, lam2, gamma, eta, V, Theta, T, p):
        '''
        Constructor that takes some parameters that define the problem
        '''
        self._w0 = w0      # initial portfolio
        self._W = W        # budget constraint
        self._mu = mu      # asset returns
        self._Sig = Sig    # asset return covariance matrix
        
        self._lam1 = lam1   # lagrange multiplier 1 (lambda)
        self._lam2 = lam2   # lagrange multiplier 2 (gamma)
        self._gamma = gamma # parameter in the formula of trading cost 
        self._eta = eta     # parameter in the formula of trading cost 
        
        self._V = V         # security imbalance of a particular day
        self._Theta = Theta # shares outstanding of a particular day
        self._T = T         # time duration
        self._p = p         # mid-quote prices of a particular day
    
    @staticmethod
    def sign(x):
        '''
        return the sign of a specific number
        '''
        
        if (x > 0): return 1.
        
        elif (x < 0): return -1.
        
        else: return 0.
        
    @staticmethod
    def TC(dw, gamma, sig, V, Theta, eta, T, p):
        '''
        calculates the trading cost of transaction of one specific security
        returns (permanent cost, temporary cost)
        '''
        # avoid division by zero error
        if V <= 1e-8: return 0., 0.
        
        # avoid division by zero error
        if p <= 1e-8: return 0., 0.
        
        return (gamma / 2) * sig * (dw / (V * p)) * (Theta / V)**(1/4), OptTcost.sign(dw / p) * eta * sig * np.abs((dw / (V * T * p)))**(0.6)
    
    
    @staticmethod 
    def TC_1d(dw, gamma, sig, V, Theta, eta, T, p):
        '''
        returns the first derivative of trading cost against w(portfolio wealth)
        '''
        
        # avoid division by zero error
        if dw <= 1e-8: return 0.
        if V <= 1e-8: return 0., 0.
        if p <= 1e-8: return 0., 0.
        
        result = (gamma / 2) * sig * (1 / V) * ((Theta / V)**(1/4)) + eta * sig * (np.abs(V*T)**(5/3)) * ((3 * dw / p) / (5 * np.abs(dw / p) ** (7/5)))
        
        return result / p

    @staticmethod 
    def TC_2d(dw, sig, V, eta, T, p):
        '''
        returns the second derivative of trading cost against w(portfolio wealth)
        '''
        # avoid division by zero error
        if dw <= 1e-8: return 0.
        if p <= 1e-8: return 0., 0.
        
        result = eta * sig * (np.abs(V*T)**(5/3)) * (-6 *((dw/p) ** 2)) / (25 * np.abs(dw/p) ** (17/5))
        
        return result / (p**2)
    
    def TC_all(self, dw):
        '''
        calculate the trading cost of transactions of all securities
        dw, sig, V, Theta are vectors of same length
        '''
        
        num = len(dw)
        cost = 0
        
        for i in range(num):
            
            tc_temp = OptTcost.TC(dw[i], self._gamma, np.sqrt(self._Sig[i][i]), self._V[i], self._Theta[i], self._eta, self._T, self._p[i])
            # add permanent cost and temporary cost separately
            cost += tc_temp[0] + tc_temp[1] 
        
        return cost

    def objective(self, w):
        '''
        calculates the objective function to optimize
        '''
        
        return np.dot(w, self._mu) - self._lam1 * np.dot(w, np.matmul(self._Sig, w)) - self._lam2 * self.TC_all(w - self._w0)
    
    def constraint(self, w):
        '''
        calculates the constraint function
        '''
        
        return np.sum(w) + self.TC_all(w - self._w0) - self._W
                
    def F(self, x = None, z = None):
        '''
        defines the F function for the solver
        '''
        
        n = len(self._w0)
        
        if x is None: 
            
            return 1, matrix(0., (n,1))
        
        x = np.array(x).reshape(n,)
        
        f0 = -self.objective(x)
        f1 = self.constraint(x)
            
        f = matrix([f0, f1], (2,1))
        
        dtc = []
            
        for i in range(n):
                
            dtc.append(OptTcost.TC_1d(x[i] - self._w0[i], self._gamma, np.sqrt(self._Sig[i][i]) , self._V[i], self._Theta[i], self._eta, self._T, self._p[i]))
            
        df0 = self._lam2 * np.array(dtc) + self._lam1 * 2 * np.matmul(self._Sig, x) - self._mu
        df1 = np.array(dtc) + 1.
            
        Df = matrix(np.array([df0, df1]), (2, n))
        
        if z is None:
            
            return f, Df
        
        data = []
        
        for i in range(n):
            
            data.append(OptTcost.TC_2d(x[i] - self._w0[i], np.sqrt(self._Sig[i][i]), self._V[i], self._eta, self._T, self._p[i]))
            
        H_tc = spdiags(data, 0, n, n)
        
        H = 2 * self._lam1 * z[0] * self._Sig + (self._lam2 * z[0] + z[1]) * H_tc
        
        H = matrix(H, (n, n))
        
        return f, Df, H
    
    def solve(self):
        '''
        performs the optimization
        '''
        
        return solvers.cp(self.F)['x']