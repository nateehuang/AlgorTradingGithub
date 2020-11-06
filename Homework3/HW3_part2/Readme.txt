Algo Trading & Quant Strategies Homework 3

Part 2

--------------------------------------------

I. Basic Info

--------------------------------------------

II. File List (1 package, 2 .py files, 2 .xlsx, 1 .csv) 

--------------------------------------------------

1 package: exercise2

5 files: OptTcost, Test_OptTcost, imbalance, s_p500, assignment3_part2_input

III. Steps

-------------------------------------------------------------------------------------------

Create the following package in the src directory: exercise2

Copy the following files to package dbReaders in the src directory: 

OptTcost, Test_OptTcost, imbalance, s_p500, assignment3_part2_input

Please install the following packages if necessary:

pandas, numpy, scipy, xlwings, cvxopt

---------------------------------------------------------------------------------------------

Notes:

1) 

The file Test_OptTcost.py has 2 tests to test the OptTcost class

2)

We choose 488 stocks instead of 500 because there was cleaning process in previous homework.

The data are in daily format, and I picked the trading day ‘20070628’ for testing.

3)

I choose the input parameters as follows (you can find them in assignment3_part2_input.xlsx):

w0: a vector of 10000
W: 1000000 
Eta = 0.142
Beta = 0.6
Lambda = 1
Gamma = 1
u, cov, V were taken from other parts of the homework
Theta was taken from the original sp500 excel file


There are no addition input files, or output files

