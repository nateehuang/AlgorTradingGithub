'''
Created on Mar 17, 2020

@author: natehuang
'''
import numpy as np
import pandas as pd

class statcomputer(object):
    '''
    A class that computes processing statistics
    '''

    def __init__(self, 
                 path_to_vwp330,
                 path_to_vwp400, 
                 path_to_mq, 
                 path_to_trade_size,
                 path_to_arrival,
                 path_to_terminal,
                 path_to_imbalance,
                 path_to_volume):
        '''
        Constructor
        
        Parameters
        ------
        path_to_vwp330: str
            path to the csv file with volume weigh price from 930 to 330
                   
        path_to_vwp400: str
            path to the csv file with volume weigh price from 930 to 400
            
        path_to_mq: str
            path to the csv file with 2-minute mid-quote returns
            
        path_to_trade_size: str
            path to the csv file with the trade size
            
        path_to_arrival: str
            path to the csv file with arrival price
            
        path_to_terminal: str
            path to the csv file with terminal price
            
        path_to_imbalance: str
            path to the csv file with the imbalance values
            
        path_to_volume: str
            path to the csv file with the total volume
        '''
        # read all the data in 
        self._vwp330 = pd.read_csv(path_to_vwp330, index_col=0)
        self._vwp400 = pd.read_csv(path_to_vwp400, index_col=0)
        self._trade_size = pd.read_csv(path_to_trade_size, index_col=0)
        from ast import literal_eval
        convert = {i:literal_eval for i in range(1,66)}
        self._mq = pd.read_csv(path_to_mq, index_col=0, converters=convert)
        self._arrival = pd.read_csv(path_to_arrival, index_col=0)
        self._terminal = pd.read_csv(path_to_terminal, index_col=0)
        self._imbalance = pd.read_csv(path_to_imbalance, index_col=0)
        self._volume = pd.read_csv(path_to_volume, index_col=0)
        
    def compute_lookback_adv(self):
        '''
        A function to compute 10-day look-back on average daily value
        
        Returns
        ------
        A pandas DataFrame with 10-day look-back on average daily value  
        '''
        daily_value_trade = self._vwp400 * self._trade_size
        dvt_roll_mean = daily_value_trade.rolling(10, min_periods=1, axis = 1).mean()
        return dvt_roll_mean.iloc[:,9:]
    
    def compute_lookback_std(self):
        '''
        A function to compute 10-day look-back on standard deviation of 2-minute mid-quote returns
        
        Returns
        ------
        A Pandas DataFrame with 10-day look-back on standard deviation of 2-minute mid-quote returns,
        scale back to daily standard deviation. The matrix excludes the first 9 days of the data.
        '''
        each_day_std = self._mq.applymap(lambda x: np.std([float(i) for i in x if i is not None]))
        stds = each_day_std.rolling(10, min_periods=1, axis = 1).mean()*np.sqrt(195)
        return stds.iloc[:,9:]
    
    def compute_drop_dates(self):
        '''
        A function to find the drop dates base on our criteria: a date that has more than 1% None 
        on the mid-quote returns of all the stocks on that date.
        
        Returns
        -----
        A Pandas Series with the date and the proportion of None 
        in the mid-quote returns vector for all the stocks on that date 
        '''
        numOfNone = self._mq.applymap(lambda x: x.count(None)).sum()
        lenOfAll = self._mq.applymap(len).sum()
        propOfNone = numOfNone/lenOfAll
        return propOfNone[propOfNone>0.01]
    
    def get_xdata(self, stocks=None, dates=None):
        '''
        A function creates a matrix with 4 columns: X, V, sigma, h
        
        Parameters
        -----
        stocks: list
            a list of stocks that you want to put into the xdata. 
            if None, takes all the stocks
            
        dates: list 
            a list of dates in string that you want to put into the xdata.
            if None, takes all the dates except the dates output by compute_drop_dates function
        
        Returns
        -----
        A matrix described above
        '''
        
        # The matrices below are all in size: number of stocks x number dates
        # calculate the imbalance values suggested on the homework notes: imbalance * volume weight price 400
        imb_v = self._imbalance
        # calculate average daily values
        adv = self.compute_lookback_adv()
        # calculate sigma
        sigma = self.compute_lookback_std()
        # calculate temporary impact
        g = (self._terminal - self._arrival)/2
        h = self._vwp330 - self._arrival - g
        self.temp_impact = h
        
        # selector
        if stocks is None:
            select_stocks = adv.index
        else:
            select_stocks = stocks
        if dates is None:
            select_dates = adv.columns
        else:
            select_dates = dates
        # subset the matrices and flatten them
        imb_v_vector = imb_v.loc[select_stocks, select_dates].values.flatten()
        adv_vector = adv.loc[select_stocks, select_dates].values.flatten()
        sig_vector = sigma.loc[select_stocks, select_dates].values.flatten()
        h_vector = h.loc[select_stocks, select_dates].values.flatten()
        
        # put them into one matrix
        xdata = np.append([imb_v_vector], [adv_vector], axis=0)
        xdata = np.append(xdata, [sig_vector], axis=0)
        xdata = np.append(xdata, [h_vector], axis=0)
        return xdata.T
    
    def split_active_xdata(self):
        '''
        Split the xdata into two parts, inactive and active based on the stocks volumes
        
        Returns
        -----
        (inactive xdata, active xdata): tuple
            The elements in the tuple have the same length
        '''
        volume_by_stocks = self._volume.sum(axis=1)
        midpt = volume_by_stocks.describe()['50%']
        inactive_lst = [ind for ind, val in volume_by_stocks.iteritems() if val<=midpt]
        active_lst = [ind for ind in volume_by_stocks.index if ind not in inactive_lst]
        inact_xdata = self.get_xdata(inactive_lst)
        act_xdata = self.get_xdata(active_lst)
        return inact_xdata, act_xdata
    
    def impact_to_csv(self):
        self.temp_impact.to_csv('temp_impact.csv')
    