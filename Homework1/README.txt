Algo Trading & Quant Strategies Homework 1 
--------------------------------------------

I. Basic Info
--------------------------------------------


II. File List (5 packages, 29 .py files, 2 .xlsx) 
--------------------------------------------------
packages: dbReaders, PartA, PartB, PartC, PartD

files under dbreaders: BinReader, FileManager, FileNames, TAQQuotesReader, TAQTradersReader
files under PartA: main, TradeWriter, QuoteWriter, TAQAdjust, TAQAdjustPlot, TAQCleaner, TAQCleanPlot,
				   Test_TradeWriter, Test_QuoteWriter, CircularArray, Test_CircularArray, Test_BinarySearch
				   s_p500.xlsx
files under PartB: main, ReturnComputer, Test_ReturnComputer, TAQStats, TestTAQStats, 
				   StockStatPlot, XExperiment
files under PartC: main, TradeReturn, Test_TradeReturn
files under PartD: Turnover, Risk_Return_example, s_p500.xlsx

III. Steps
-------------------------------------------------------------------------------------------
Create the following packages in the src directory: dbReaders, PartA, PartB, PartC, PartD

Copy the following files to package dbReaders in the src directory: 
BinReader, FileManager, FileNames, TAQQuotesReader, TAQTradersReader
---------------------------------------------------------------------------------------------
| Change the attributes TAQR in FileNames.py to your local directory which contains TAQ data |
---------------------------------------------------------------------------------------------

Copy the following files to package PartA in the src directory: 
main, TradeWriter, QuoteWriter, TAQAdjust, TAQAdjustPlot, TAQCleaner, TAQCleanPlot,
Test_TradeWriter, Test_QuoteWriter, CircularArray, Test_CircularArray, Test_BinarySearch, s_p500.xlsx
When run, TAQAdjust will create files in PartA directory while TAQCleaner will create files in the source directory

Copy the following files to package PartB in the src directory:
main, ReturnComputer, Test_ReturnComputer, TAQStats, TestTAQStats, StockStatPlot

Copy the following files to package PartD in the src directory:
Turnover, Risk_Return_example, s_p500.xlsx
(Please make sure CVXOPT is correctly installed before running the programs)

The file Test_TradeWriter.py has 1 test to test the TradeWriter class
The file Test_QuoteWriter.py has 1 test to test the QuoteWriter class
The file Test_CircularArray.py has 1 test to test the CircularArray class
The file Test_TAQStats.py has 1 test to test the TAQStats class
The file Test_ReturnComputer.py has 1 test to test the ReturnComputer class
The file Test_TradeReturn.py has 1 test to test the TradeReturn class

There are no addition input files, or output files