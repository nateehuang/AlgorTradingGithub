'''
Created on Mar 21, 2020

@author: natehuang
'''
import numpy as np
import pandas as pd

class regression(object):
    '''
    '''

    def __init__(self, filepath=None, statSource=None):
        '''
        Parameters
        -----
        filepath: str
            Path to read a csv file formatted as assignment2_part_1_input.csv provided by the TA.
            If this is None, statSource must not be None.
            
        statSource: statcomputer
            A statcomputer class that provides xdata for regression.
            If None, filepath must not be None.
        '''
        if filepath is None:
            self._xdata = statSource.get_xdata()
        else:
            # if a csv file is provided, read the file
            df = pd.read_csv(filepath, header = None)
            table_names = ['Day0', 'Day1', 'Day2']
            groups = df[0].isin(table_names).cumsum()
            xdata = np.array([[None, None, None, None]])
            for _, g in df.groupby(groups):
                xdata = np.append(xdata, g.iloc[1:10, 1:].to_numpy(), axis=0)
            self._xdata = xdata[1:].astype(np.float)
    
    @staticmethod
    def impact_cost_fun(x, imb_v, adv, std, y):
        '''
        Cost function for the nonlinear regression
        
        Parameters
        -----
        x: list
            A list where the first value is eta, second value is beta
            
        std: np.array
            10-day look-back standard deviation in one long array
            
        imb_v: np.array
            imbalance value in one long array
            
        adv: np.array
            average daily value in one long array
            
        y: np.array
            the temporary impact in one long array
            
        Returns
        -----
        res_lsq.x: list
            list of optimal parameters
        '''
        return (x[0]*std*np.sign(imb_v)*np.abs(imb_v/((6/6.5)*adv))**x[1])-y
        
    def compute_eta_beta(self, fun, x0=[1,1], xdata=None):
        '''
        '''
        from scipy.optimize import least_squares
        record = False
        # If there is no other source of data, use xdata in the class
        if xdata is None:
            xdata = self._xdata
            record = True
        res_lsq = least_squares(fun, x0, args = (xdata[:, 0],
                                                 xdata[:, 1],
                                                 xdata[:, 2],
                                                 xdata[:, 3]), 
                                                 bounds=((-np.inf, 0), (np.inf, np.inf)), 
                                                 loss='soft_l1')
        # keep a record of the optimal parameters, residual and jacobian
        if record:
            self._x = res_lsq.x
            self._residual = res_lsq.fun
            self._jac = res_lsq.jac
        return res_lsq.x, res_lsq.jac, res_lsq.fun
    
    def compute_t_stat(self, x=None, jaco=None, residual=None):
        '''
        Compute the t-statistics for the estimated parapmeters
        
        Returns
        -----
        standard_tstat: float
            t-stat using standard errors
            
        robust_tstat: float
            t-stat using robust errors
            
        standard_cov.diagonal(): np.array
            Variances of the estimated parameters using standard errors
            
        robust_cov.diagonal(): np.array
            Variance matrix of the estimated parameters using the robust errors
        '''
        # calculating robust_tstat
        record = False
        if x is None:
            x = self._x
        if jaco is None:
            jaco = self._jac
            record = True
        hess = jaco.T@jaco
        if residual is None:
            residual = np.diag(self._residual)
        else:
            residual = np.diag(residual)
        residual_sq = residual**2
        robust_cov = np.linalg.inv(hess)@jaco.T@residual_sq@jaco@np.linalg.inv(hess)
        robust_std = np.sqrt([robust_cov[0,0], robust_cov[1,1]])
        robust_tstat = x/robust_std
        if record:
            self._robust_std = robust_std
            self._robust_tstat = robust_tstat
        
        # calculating standard tstat
        var_residual = np.sum(residual_sq/(residual_sq.shape[0]-2))
        standard_cov = var_residual*np.linalg.inv(jaco.T@jaco)
        standard_std = np.sqrt([standard_cov[0,0], standard_cov[1,1]])
        standard_tstat = x/standard_std
        if record:
            self._standard_std = standard_std
            self._standard_tstat = standard_tstat
        print("t statistics using standard errors are ", standard_tstat)
        print("t statistics using heteroskedasticity-robust errors are ", robust_tstat)
        return standard_tstat, robust_tstat, standard_cov.diagonal(), robust_cov.diagonal()
    
    def stat_significant(self, tstat=None, df=None, alpha=0.05):
        '''
        Parameters
        -----
        alpha: float
            significance, default 0.05
        
        Returns
        -----
        list of boolean
            boolean values about whether the parameters [eta, beta] are statistically significant
        '''
        from scipy.stats import t
        if tstat is None:
            tstat = self._robust_tstat
        if df is None:
            df = self._residual.shape[0]-2
        c_val = t.ppf(1-alpha/2, df=df)
        print("95% confident statistically significant: ", tstat>c_val)
        return tstat>c_val
    
    def residual_plot(self):
        '''
        Plot the residual and save it to current directory
        '''
        import matplotlib.pyplot as plt
        from scipy.stats import norm
        from statsmodels.graphics.gofplots import qqplot
        # set the size of the plot
        plt.figure(figsize=(16,9))
        # plot the distribution
        ax = plt.subplot(121)
        # create bins and count the numbers
        count = pd.DataFrame([0]*24, index=np.arange(-5.75, 6, step=0.5))
        for i in count.index:
            for r in self._residual:
                if r>=i-0.25 and r<i+0.25:
                    count.loc[i] += 1
        # create a normal distribution reference
        xx = np.linspace(-3, 3, 100)
        normal = norm.pdf(xx, np.mean(self._residual), np.std(self._residual))
        normalcdf = norm.cdf(xx, np.mean(self._residual), np.std(self._residual))
        low_flag = True
        for i in range(xx.shape[0]):
            if normalcdf[i]>=0.025 and low_flag:
                low = i
                low_flag = False
            if normalcdf[i]>=0.975:
                high = i
                break
        # plot the distribution
        plt.plot(count.index, count, 'o', label="residual")
        plt.plot(xx, normal*self._residual.shape[0], '--', label="normal")
        plt.fill_between(xx[low:high], 0, normal[low:high]*self._residual.shape[0], alpha=.3, facecolor="grey", label="95% normal")
        plt.xlim([-6, 6])
        ax.set_ylim(bottom=5)
        ax.legend()
        plt.title("Distribution of the residual")
        plt.yscale('log')
        # plot the QQ plot
        ax = plt.subplot(122)
        qqplot(self._residual, line='s', ax=ax)
        plt.xlim([-3.5,3.5])
        plt.ylim([-5, 5])
        plt.title("residual QQ plot")
        #plt.show()
        plt.savefig("residual_plots.png")
        
    def active_inactive(self, dataSource):
        '''
        Analyze the parameters obtained from active stocks and inactive stocks
        
        Returns
        -----
        Parameters based on inactive stocks
        
        Inactive parameters t-statistics
        
        Inactive parameters significance based on robust errors
        
        Parameters based on active stocks
        
        Active parameters t-statistics
        
        Active parameters significance based on robust errors
        '''
        print("---------------")
        # get the inactive and active data
        self._inactive, self._active = dataSource.split_active_xdata()
        # compute the inactive parameter, t-statistics...
        inact_param, inact_jac, inact_residual = self.compute_eta_beta(self.impact_cost_fun, xdata=self._inactive)
        print("The parameters based on inactive stocks are ", inact_param)
        inact_tstat_std, inact_tstat_rob, inact_cov_std, inact_cov_rob = self.compute_t_stat(x=inact_param, jaco=inact_jac, residual=inact_residual)  # @UnusedVariable
        inact_stat_sig = self.stat_significant(tstat=inact_tstat_rob, df=inact_jac.shape[0])  # @UnusedVariable
        # compute the active parameter, t-statistics...
        act_param, act_jac, act_residual = self.compute_eta_beta(self.impact_cost_fun, xdata=self._active)
        print("The parameters based on active stocks are ", act_param)
        act_tstat_std, act_tstat_rob, act_cov_std, act_cov_rob = self.compute_t_stat(x=act_param, jaco=act_jac, residual=act_residual)  # @UnusedVariable
        act_stat_sig = self.stat_significant(tstat=act_tstat_rob, df=act_jac.shape[0])  # @UnusedVariable
        
        z = (inact_param - act_param)/(np.sqrt(inact_cov_rob+act_cov_rob))
        print("The z statistics is ", z)
        from scipy.stats import norm
        low, high = norm.ppf(0.025), norm.ppf(0.975)
        if z[0] < low or z[0] > high:
            print("eta estimated from inactive and active stocks are different with 95% confidence level")
        else:
            print("eta estimated from inactive and active stocks are the same with 95% confidence level")
            
        if z[1] < low or z[1] > high:
            print("beta estimated from inactive and active stocks are different with 95% confidence level")
        else:
            print("beta estimated from inactive and active stocks are the same with 95% confidence level")
        
        