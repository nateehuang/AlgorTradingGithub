'''
Created on Feb 22, 2020
@author: Nate, Zibin, Martin

Class to unzip file and generate adjusted files, which save at within the folder PartA
'''

import os
import shutil
import pandas as pd
from dbReaders.FileNames import FileNames
from dbReaders.FileManager import FileManager
from PartA.TradeWriter import TradeWriter
from PartA.QuoteWriter import QuoteWriter

def unzipFiles(path, do = False):
    '''
    Unpack files from the trade.zip and quote.tar.gz
    '''
    if do:
        print("Unzipping", path)
        for fileName in os.listdir(path):
            if fileName.endswith(".zip") or fileName.endswith(".gz"):
                shutil.unpack_archive(path + "/" + fileName, path)
                


class Adjuster(object):
    '''
    Adjust TAQ data and save them into binary files
    '''

    def __init__(self, refXlsx = "s_p500.xlsx", startDateString="20070620", endDateString="20070921"):
        '''
        Parameters
        ------
        refXlsx : str
            The excel file used to get the factors, the file should be in the same directory of this py file
        
        startDateString : str
            The starting date of the data (default 20070620)
            
        endDateString : str
            The end date of the data (default 20070921)
        '''
        self._refFile = refXlsx
        # a pd.df saving the necessary info from the excel
        self._ref = (
            pd.read_excel(self._refFile, dtype=str).dropna(subset=["Ticker Symbol"])
            [["PERMNO", 
              "Names Date", 
              "Ticker Symbol", 
              "Cumulative Factor to Adjust Prices", 
              "Cumulative Factor to Adjust Shares/Vol"]]
            )
        # a list of permanent numbers
        self._ref["PERMNO"] = self._ref["PERMNO"].astype(int)
        # a list of Price adjust factors
        self._ref["Cumulative Factor to Adjust Prices"] = self._ref["Cumulative Factor to Adjust Prices"].astype(float)
        # a list of shares adjust factors
        self._ref["Cumulative Factor to Adjust Shares/Vol"] = self._ref["Cumulative Factor to Adjust Shares/Vol"].astype(float)
        # the base directory of the TAQ data
        self._baseDir = FileNames.TAQR
        # file manager help to read TAQ
        self._fm = FileManager( self._baseDir )
        self._dates = self._fm.getTradeDates(startDateString, endDateString) # 20070620, 20070621, ...
        # sort the date in order
        self._dates.sort()
        # the directory to save the trade data, if not exist, create directory
        self._tradeDestination = os.getcwd()+"/adjusted_trades"
        if not os.path.isdir(self._tradeDestination):
            os.mkdir(self._tradeDestination)
        # the directory to save the quote data, if not exist, create directory 
        self._quoteDestination = os.getcwd()+"/adjusted_quotes"
        if not os.path.isdir(self._quoteDestination):
            os.mkdir(self._quoteDestination)

    def filterSP500(self, ):
        # return a list of lists of SP500 ticker on date range
        # this is a pd.Series of lists of Ticker Symbol on different dates
        group = self._ref.groupby("Names Date")
        self._spTickers = group["Ticker Symbol"].apply(list)
        self._permno = group["PERMNO"].apply(list)

        
    def adjust(self, save = False):
        priceAdjustLs = self._ref.groupby("Ticker Symbol").filter(
            lambda x: x["Cumulative Factor to Adjust Prices"].value_counts().shape[0]>1)["Ticker Symbol"].unique()
        print("The tickers which have adjust Cumulative Factor to Adjust Prices are ", priceAdjustLs)
        shareAdjustLs = self._ref.groupby("Ticker Symbol").filter(
            lambda x: x["Cumulative Factor to Adjust Shares/Vol"].value_counts().shape[0]>1)["Ticker Symbol"].unique()
        print("The tickers which have adjust Cumulative Factor to Adjust Shares/Vol are ", priceAdjustLs)
        
        # Adjust the price and save trade and quote data
        # based on stock in one file
        # write content in
        if save:
            # loop over the dates
            for date in self._dates:
                print("Adjusting ", date)
                # get the tickers on that date
                tickers = self._spTickers[date]
                # get the permanent numbers of the date
                permno = self._permno[date]
                # get the factors of the date
                factors = self._ref[self._ref["Names Date"]==date]
                # loop over the SP500 tickers, read the TAQ data, adjust and then save them
                for per, tick in zip(permno, tickers):
                    # instantiate writers
                    tradeWriter = TradeWriter(os.path.join(self._tradeDestination, tick+"_trades.gz"), per)
                    quoteWriter = QuoteWriter(os.path.join(self._quoteDestination, tick+"_quotes.gz"), per)
                    # adjust the data within the adjust data list
                    if tick in priceAdjustLs or tick in shareAdjustLs:
                        priceFactor = factors.loc[factors["Ticker Symbol"]==tick, 
                                              "Cumulative Factor to Adjust Prices"].iloc[0]
                        shareFactor = factors.loc[factors["Ticker Symbol"]==tick, 
                                              "Cumulative Factor to Adjust Shares/Vol"].iloc[0]
                    else:
                        priceFactor = 1
                        shareFactor = 1
                    # save the data
                    if os.path.isfile(os.path.join(FileNames.BinRTTradesDir, date, tick+"_trades.binRT")):
                        trade = self._fm.getTradesFile(date, tick)
                        tradeWriter.writer(trade, priceFactor, shareFactor)
                    if os.path.isfile(os.path.join(FileNames.BinRQQuotesDir, date, tick+"_quotes.binRQ")): 
                        quote = self._fm.getQuotesFile(date, tick)
                        quoteWriter.writer(quote, priceFactor, shareFactor)                    


                        