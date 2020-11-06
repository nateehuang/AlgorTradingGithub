'''
Created on Mar 16, 2020

@author: Zibin
'''
import os
from ImpactModel.MatrixToCSV import MatrixToCSV
from ImpactModel.StatisticsComputer import statcomputer
from ImpactModel.Regression import regression
from ImpactModel.Elimination import deleteFile

if __name__ == '__main__':
    
    def discardStock():
        # check if each stock has any missing value
        # if yes, then remove the ticker data from folder
        # run approximate 3 hours
        discardTicker = deleteFile() # a list of tickers that will be discarded
        return discardTicker
    
    def usedStock():
        '''
        Generate a list that contains all the tickers that we use
        '''
        usedTicker = []
        parentDir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
        tradePath = parentDir + '/clean_trades/'
        for filename in sorted(os.listdir(tradePath)):
            if filename.endswith('.gz'): # exclude DS.store
                usedTicker.append(filename[:-10])
        return usedTicker
       
    def CSV():
        '''
        Function to generate CSV
        '''
        nameOption = ['totalVolume', 'imbalance', 'VWAP330', 'VWAP400', \
                      'arrivalPrice', 'terminalPrice', 'twoMinReturn', 'numShare']        
        for name in nameOption:
            obj = MatrixToCSV(name)
            mat = obj.matrixGenerator()
            obj.csvGenerator(mat)
    
    print(os.getcwd())
    sc = statcomputer(path_to_vwp330='VWAP330.csv',
                 path_to_vwp400='VWAP400.csv', 
                 path_to_mq='twoMinReturn.csv', 
                 path_to_trade_size='numShare.csv',
                 path_to_arrival='arrivalPrice.csv',
                 path_to_terminal='terminalPrice.csv',
                 path_to_imbalance='imbalance.csv',
                 path_to_volume='totalVolume.csv')
    reg = regression(statSource=sc)
     
    print("The parameters [eta, beta] are ", reg.compute_eta_beta(regression.impact_cost_fun)[0])
    reg.compute_t_stat()
    reg.stat_significant()
    reg.active_inactive(dataSource=sc)
    reg.residual_plot()