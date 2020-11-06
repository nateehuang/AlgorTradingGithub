'''
Created on Apr 6, 2020

@author: huang
'''
import numpy as np
import pandas as pd
import pyRMT

class Covariance(object):
    '''
    classdocs
    '''

    def __init__(self, returnMat=None, path=None):
        '''
        Parameters
        -----
        returnMat: ndarray, shape(n_sample, n_stocks)
            A matrix of return, if None, path must not be None
            
        path: ndarray, shape(n_stocks, n_dates)
            A path to the csv file list of 5 minutes return of stocks and dates
            if None, returnMat must not be None
        '''
        if path is None:
            self._returnMat = returnMat
            self._length = returnMat.shape[1]
        elif returnMat is None:
            # read the matrix in
            from ast import literal_eval
            convert = {i:literal_eval for i in range(1,66)}
            Mat = pd.read_csv(path, index_col=0, converters=convert)
            indices = Mat.index
            m = []
            # clean the matrix
            for ind in indices:
                # exclude 20070703 since too many None
                sub = [e for d in Mat.loc[ind, Mat.columns!='20070703'] for e in d if e is not None]
                m.append(sub)
            # based on the length of the 5-minute returns of each stock, 
            # discard 1% of the stock because they have too few number of returns
            threshold = np.percentile(list(map(len,m)), 1)
            m1 = [s for s in m if len(s)>threshold]
            self._length = min(map(len, m1))
            m2 = np.array([s[:self._length] for s in m1])
            # standardize the matrix
            sample_mean = m2.mean(axis = 1).reshape(m2.shape[0], 1)
            # compute cross session volatility
            cross_vol = np.apply_along_axis(lambda x: np.sqrt((x**2).sum()), 0 , m2)
            m3 = (m2-sample_mean)/cross_vol
            # center the return vector 
            self._returnMat = np.array(m3)
        self._daily_sample_num = int(np.floor(self._length/64))
        # there are 78 five minutes in one day(9:30 to 16:00, 6.5 hours), 252 trading days in one year
        self._standarized_factor = 78*252
    
    def rolling(self, covariance_cleaning):
        '''
        Compute the volatility with standard error based on three predictors: Empirical, Clipped, RIE optimalShrinkage
        
        Parameters
        -----
        covariance_cleaning: func
            function to compute the clean covariance
            
        Returns
        -----
        res: list
            list contains volatility and standard error of the three predictors
        '''
        mvp_vols = []
        omniscient_vols = []
        random_vols = []
        start = 0
        end = self._daily_sample_num * 15
        # training set has 15 days of data
        # out of sample set has 1 day of data
        # rolling from day 1
        while end + self._daily_sample_num < self._length:
            training = self._returnMat[:, start:end].T
            ofs = self._returnMat[:, end:end+self._daily_sample_num]
            # use the mean of the out of sample return in a day
            cov_est_inv = np.linalg.inv(covariance_cleaning(training))
            mvp_vols.append(self.mvp(cov_est_inv, ofs))
            omniscient_vols.append(self.omniscient(cov_est_inv, ofs,))
            random_vols.append(self.random(cov_est_inv, ofs))
                
            start, end = start+self._daily_sample_num, end + self._daily_sample_num
        res = []
        res.append([np.mean(mvp_vols), np.std(mvp_vols)])
        res.append([np.mean(omniscient_vols), np.std(omniscient_vols)])
        res.append([np.mean(random_vols), np.std(random_vols)])
        return res
    
    def mvp(self, cov_est_inv, real,):
        '''
        calculate the volatility of out of sample minimum variance portfolio
        
        Parameters
        -----
        cov_est: ndarray
            Covariance estimate of the stocks
            
        real: ndarray
            out of sample return matrix
            
        Returns
        -----
        Standard deviation of the return
        '''
        g = np.ones([cov_est_inv.shape[0], 1])
        weight = cov_est_inv@g/(g.T@cov_est_inv@g)
        # standardize the weight vector to 1
        w = weight/weight.sum()
        rets = w.T@real 
        return np.std(rets)
    
    def omniscient(self, cov_est_inv, real,):
        '''
        compute the volatility of out of sample omniscient predictor
        
        Parameters
        -----
        cov_est: ndarray
            Covariance estimate of the stocks
            
        real: ndarray
            out of sample return matrix
            
        Returns
        -----
        Standard deviation of the return
        '''
        ofs_ret = real.sum(axis=1)
        g = np.sqrt(ofs_ret.shape[0])*ofs_ret
        weight = cov_est_inv@g/(g.T@cov_est_inv@g)
        # standardize the weight vector to 1
        w = weight/weight.sum()
        rets = w.T@real 
        return np.std(rets)
    
    def random(self, cov_est_inv, real):
        '''
        compute the volatility of out of sample random predictor
        
        Parameters
        -----
        cov_est: ndarray
            Covariance estimate of the stocks
            
        real: ndarray
            out of sample return matrix
            
        Returns
        -----
        Standard deviation of the return
        '''
        ran = np.random.rand(cov_est_inv.shape[0], 1) - 0.5
        v = ran/np.linalg.norm(ran)
        g = np.sqrt(cov_est_inv.shape[0]) * v
        weight = cov_est_inv@g/(g.T@cov_est_inv@g)
        # standardize the weight vector to 1
        w = weight/weight.sum()
        rets = w.T@real
        return np.std(rets)
    
    def computeEmpirical(self, train):
        '''
        compute the empirical estimate covariance 
        
        Parameters
        -----
        train: ndarray
            training data
            
        Return
        -----
        empirical estimate covariance
        '''
        from sklearn import covariance
        # calculate annualized covariance
        empirical = covariance.empirical_covariance(train, assume_centered=True) 
        return empirical * self._standarized_factor
    
    def computeClipped(self, train):
        '''
        compute the clipped estimate covariance 
        
        Parameters
        -----
        train: ndarray
            training data
            
        Return
        -----
        empirical estimate covariance
        '''
        clipped = pyRMT.clipped(train, return_covariance=True)
        return clipped * self._standarized_factor
        
    def computeOptimalShrinkage(self, train):
        '''
        compute the RIE optimal shrinkage estimate covariance 
        
        Parameters
        -----
        train: ndarray
            training data
            
        Return
        -----
        empirical estimate covariance
        '''
        optimalShrinkage = pyRMT.optimalShrinkage(train, return_covariance=True)
        return optimalShrinkage * self._standarized_factor
    
    def output_table_A(self):
        '''
        create a table similar to table A on the paper "Cleaning correlation matrices"
        '''
        clean = {'Empirical':self.computeEmpirical, 'Clipped':self.computeClipped, 'RIE Optimal Shrinkage':self.computeOptimalShrinkage}
        res = dict()
        for k, v in clean.items():
            print("Computing ", k)
            res[k] = self.rolling(v)
        df = pd.DataFrame(res, index=['Minimum Variance portfolio', 'Omniscient predictor', 'Random predictor'])
        df1 = df.applymap(lambda x: str(round(x[0]*100,2)) + ' (' + str(round(x[1]*100, 2)) + ')').T
        print(df1)
        df1.to_csv('tableA.csv')
    