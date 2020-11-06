'''
Created on Feb 24, 2020

@author: Nate, Zibin, Martin

The program reads an excel file that contains S&P 500 stock data. From 06/20/2007 to 09/20/2007, 
it calculates the daily weight for each stock in the "market portfolio". Finally, it uses the weights
to calculate the turnover rate between the two dates. Results are printed at the end.
'''

import pandas as pd
import numpy as np

# the path of excel file that contains all the original data
# assume the file in the same package
excelFile = ("s_p500.xlsx")

# read file as pandas dataframe
sp500 = pd.read_excel(excelFile, dtype=str).dropna(subset=['Ticker Symbol', 'Names Date', 'Price or Bid/Ask Average', 'Shares Outstanding'])

# get four columns 
sp500 = sp500[['Names Date','Ticker Symbol','Price or Bid/Ask Average', 'Shares Outstanding']]

# convert price and share column values to numeric values
# fill empty spaces with zeros
sp500['Price or Bid/Ask Average'] = pd.to_numeric(sp500['Price or Bid/Ask Average'], errors='coerce').fillna(0.)
sp500['Shares Outstanding'] = pd.to_numeric(sp500['Shares Outstanding'], errors='coerce').fillna(0)

# get three series separately for ticker, price and shares outstanding
sp500_tickers = sp500.groupby('Names Date')['Ticker Symbol'].apply(list)
sp500_prices = sp500.groupby('Names Date')['Price or Bid/Ask Average'].apply(list)
sp500_shares = sp500.groupby('Names Date')['Shares Outstanding'].apply(list)

# get an array of date strings from 06/20/2007 to 09/20/2007
sp500_dates = np.asarray(sp500_tickers.index)

# get the common tickers for each trading date
flag = True
for tickers in sp500_tickers:
    if flag:
        set_tickers = set(tickers)
        flag = False
        continue
    set_tickers = set_tickers.intersection(set(tickers))

# identify the positions of uncommon tickers with their shares and prices
element_removed = []
for date in sp500_dates:
    list_now = sp500_tickers[date]
    
    for i in range(len(list_now)):
        ticker = list_now[i]
        if not ticker in set_tickers:
            element_removed.append((date, i))

# clean the prices series to let each date has the same length
for pair in element_removed:
    date = pair[0]
    index = pair[1]
    
    # mark the position to remove
    sp500_prices[date][index] = 'd'

for l in sp500_prices:
    while('d' in l):
        l.remove('d')

# clean the shares array to let each date has the same length
for pair in element_removed:
    date = pair[0]
    index = pair[1]
    
    # mark the position to remove
    sp500_shares[date][index] = 'd'

for l in sp500_shares:
    while('d' in l):
        l.remove('d')

# clean the tickers series to let each date has the same length
for pair in element_removed:
    date = pair[0]
    index = pair[1]
    
    sp500_tickers[date][index] = 'd'

for l in sp500_tickers:
    while('d' in l):
        l.remove('d')
        
'''
This function takes in a list, removes all duplicates in the list

returns the edited list and a list of zero-based indices of 
    the removed elements
'''
def rm_dup(l):
    
    res = [] 
    idx = []
    
    j = 0
    for i in l: 
        if i not in res: 
            res.append(i) 
        else:
            idx.append(j)
        j += 1
        
    return res, idx

#final adjustment of the data; remove over-counted elements
for date in sp500_dates:
    sp500_tickers[date], idx = rm_dup(sp500_tickers[date])
    
    a1 = sp500_prices[date]
    a2 = sp500_shares[date]
    
    for j in idx:
        a1[j] = 'd'
        a2[j] = 'd'
    
    while ('d' in a1):
        a1.remove('d')
        
    while ('d' in a2):
        a2.remove('d')

# calculate the portfolio holdings (stock weights) for each date
sp500_weights = pd.Series(dtype = 'float64')

for date in sp500_dates:
    price_array = np.asarray(sp500_prices[date])
    share_array = np.asarray(sp500_shares[date])
    
    capital_array = np.multiply(price_array, share_array)
    capital_total = np.sum(capital_array)
    weight_array = capital_array / capital_total
    sp500_weights[date] = weight_array

# calculate the turnover rate
array_temp = [0]*(len(sp500_weights.index) - 1)

for i in range(1, len(sp500_weights.index)):
    array_next = np.asarray(sp500_weights[i])
    array_prev = np.asarray(sp500_weights[i-1])
    
    array_temp[i-1] =  np.subtract(array_next, array_prev)

# the array that contains weight differences between each date for each stock
array_temp = np.array(array_temp)

# sum up the absolute value of the weight differences and divide it by number of trading days
turnover = np.sum(np.absolute(array_temp))
num_trading_days = len(sp500_dates)
turnover = turnover / num_trading_days

# print the result
s1 = '20070620'
s2 = '20070920'

port = {s1 : pd.Series(sp500_weights[s1]), s2 : pd.Series(sp500_weights[s2])}
result = pd.DataFrame(port)
result.index = sp500_tickers[s1]

print(result.T)
print('\n')

print('The turnover of market portfolio between the two dates is ')
print(turnover)