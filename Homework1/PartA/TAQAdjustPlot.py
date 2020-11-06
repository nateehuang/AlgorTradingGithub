'''
Created on Feb 23, 2020

@author Nate, Zibin, Martin
'''

from dbReaders.TAQTradesReader import TAQTradesReader
from dbReaders.TAQQuotesReader import TAQQuotesReader
from dbReaders.BinReader import BinReader
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

'''File to plot two adjusted stocks'''

plot = False # If change to True, running the program will produce graph 

def ori_vs_adj_trade_NVDA():
    dayStartNVDA = '20070910' # Start day
    dayEndNVDA = '20070911' # End day
    
    parentddir1 = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    parentddir2 = os.path.abspath(os.path.join(parentddir1, os.path.pardir))

    oriTradeStartNVDA = TAQTradesReader(os.path.join(parentddir2, 'R/trades/'+dayStartNVDA+'/NVDA_trades.binRT'))
    oriTradeEndNVDA = TAQTradesReader(os.path.join(parentddir2, 'R/trades/'+dayEndNVDA+'/NVDA_trades.binRT'))
    
    oriPriceNVDA = [] # List to store price
    oriShareNVDA = [] # List to store number of shares
    timeList = [] # List to store time stamp
    
    # Append data to each of the lists
    for i in range(oriTradeStartNVDA.getN()):
        oriPriceNVDA.append(oriTradeStartNVDA.getPrice(i))
        oriShareNVDA.append(oriTradeStartNVDA.getSize(i))
        timeList.append(1189396800000 + oriTradeStartNVDA.getTimestamp(i))
    
        
    for i in range(oriTradeEndNVDA.getN()):
        oriPriceNVDA.append(oriTradeEndNVDA.getPrice(i))
        oriShareNVDA.append(oriTradeEndNVDA.getSize(i))
        timeList.append(1189483200000 + oriTradeEndNVDA.getTimestamp(i))
    
    # convert data format to datetime
    dateTimeList = []
    for timeStamp in timeList:
        dateTimeList.append(datetime.fromtimestamp(timeStamp/1000))
    
    adjTradeStartNVDA = BinReader(os.path.join(os.getcwd(), 'adjusted_trades/NVDA_trades.gz'), '>QIIf', 100)
    ts0, _, size0, p0 = adjTradeStartNVDA.next()
    
    ts = []
    ts.append(ts0)
    share = []
    share.append(size0)
    price = []
    price.append(p0)
    
    while adjTradeStartNVDA.hasNext():
        t, i, s, p = adjTradeStartNVDA.next()
        ts.append(t)
        share.append(s)
        price.append(p)
    
    sIdx = binarySearch(ts, 0, len(ts)-1, timeList[0]) # find the start index
    eIdx = binarySearch(ts, 0, len(ts)-1, timeList[-1])  # find the end index
    
    pList = price[sIdx:eIdx+1]
    sList = share[sIdx:eIdx+1]
    
    adjTradeStartNVDA.close() # close bin reader
      
    plt.figure(figsize=(9,6))
    ax = plt.gca()
    xfmt = mdates.DateFormatter('%m-%d %H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(dateTimeList[:-5], oriPriceNVDA[:-5], ls = 'None', marker = 'o', ms = 5, color = 'y', label = 'original')
    plt.plot(dateTimeList[:-5], pList, ls = 'None', marker = 'x', ms = 2 , color = 'black', label = 'adjusted')
    plt.xticks([datetime.strptime('2007-09-10 10:00:00', '%Y-%m-%d %H:%M:%S'), 
                datetime.strptime('2007-09-10 15:00:00', '%Y-%m-%d %H:%M:%S'),
                datetime.strptime('2007-09-11 09:30:00', '%Y-%m-%d %H:%M:%S'), 
                datetime.strptime('2007-09-11 15:00:00', '%Y-%m-%d %H:%M:%S')])
    plt.title('Original NVDA Trade Price VS Adjusted NVDA Trade Price')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
     
    plt.figure(figsize=(9,6))
    ax = plt.gca()
    xfmt = mdates.DateFormatter('%m-%d %H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(dateTimeList[:-5], oriShareNVDA[:-5], ls = 'None', marker = 'o', ms = 5, color = 'y', label = 'original')
    plt.plot(dateTimeList[:-5], sList, ls = 'None', marker = 'x', ms = 2 , color = 'black', label = 'adjusted')
    plt.xticks([datetime.strptime('2007-09-10 10:00:00', '%Y-%m-%d %H:%M:%S'), 
                datetime.strptime('2007-09-10 15:00:00', '%Y-%m-%d %H:%M:%S'),
                datetime.strptime('2007-09-11 09:30:00', '%Y-%m-%d %H:%M:%S'), 
                datetime.strptime('2007-09-11 15:00:00', '%Y-%m-%d %H:%M:%S')])
    plt.ylim(0,10000)
    plt.title('Original NVDA Trade Share VS Adjusted NVDA Trade Share')
    plt.xlabel('Time')
    plt.ylabel('Number of Shares')
    plt.legend()
    plt.show()
 
def ori_vs_adj_trade_MTW():
    dayStartMTW = '20070910' # Start day
    dayEndMTW = '20070911' # End day
    
    parentddir1 = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    parentddir2 = os.path.abspath(os.path.join(parentddir1, os.path.pardir))
    
    oriTradeStartMTW = TAQTradesReader(os.path.join(parentddir2, 'R/trades/'+dayStartMTW+'/MTW_trades.binRT'))
    oriTradeEndMTW = TAQTradesReader(os.path.join(parentddir2, 'R/trades/'+dayEndMTW+'/MTW_trades.binRT'))
    
    oriPriceMTW = [] # List to store price
    oriShareMTW = [] # List to store number of shares
    timeList = []
    
    # Append data to each of the lists
    for i in range(oriTradeStartMTW.getN()):
        oriPriceMTW.append(oriTradeStartMTW.getPrice(i))
        oriShareMTW.append(oriTradeStartMTW.getSize(i))
        timeList.append(1189396800000 + oriTradeStartMTW.getTimestamp(i))
    
        
    for i in range(oriTradeEndMTW.getN()):
        oriPriceMTW.append(oriTradeEndMTW.getPrice(i))
        oriShareMTW.append(oriTradeEndMTW.getSize(i))
        timeList.append(1189483200000 + oriTradeEndMTW.getTimestamp(i))
    
    dateTimeList = []
    for timeStamp in timeList:
        dateTimeList.append(datetime.fromtimestamp(timeStamp/1000))
    
    adjTradeStartMTW = BinReader(os.path.join(os.getcwd(), 'adjusted_trades/MTW_trades.gz'), '>QIIf', 100)
    ts0, _, size0, p0 = adjTradeStartMTW.next()
    
    ts = []
    ts.append(ts0)
    share = []
    share.append(size0)
    price = []
    price.append(p0)
    
    while adjTradeStartMTW.hasNext():
        t, i, s, p = adjTradeStartMTW.next()
        ts.append(t)
        share.append(s)
        price.append(p)
    
    sIdx = binarySearch(ts, 0, len(ts)-1, timeList[0])
    eIdx = binarySearch(ts, 0, len(ts)-1, timeList[-1])
    
    pList = price[sIdx:eIdx+1]
    sList = share[sIdx:eIdx+1]
    
    adjTradeStartMTW.close()
      
    plt.figure(figsize=(9,6))
    ax = plt.gca()
    xfmt = mdates.DateFormatter('%m-%d %H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(dateTimeList[:-1], oriPriceMTW[:-1], ls = 'None', marker = 'o', ms = 5, color = 'y', label = 'original')
    plt.plot(dateTimeList[:-1], pList, ls = 'None', marker = 'x', ms = 2 , color = 'black', label = 'adjusted')
    plt.xticks([datetime.strptime('2007-09-10 10:00:00', '%Y-%m-%d %H:%M:%S'), 
                datetime.strptime('2007-09-10 15:00:00', '%Y-%m-%d %H:%M:%S'),
                datetime.strptime('2007-09-11 09:30:00', '%Y-%m-%d %H:%M:%S'), 
                datetime.strptime('2007-09-11 15:00:00', '%Y-%m-%d %H:%M:%S')])
    plt.title('Original MTW Trade Price VS Adjusted MTW Trade Price')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
    
    plt.figure(figsize=(9,6))
    ax = plt.gca()
    xfmt = mdates.DateFormatter('%m-%d %H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(dateTimeList[:-1], oriShareMTW[:-1], ls = 'None', marker = 'o', ms = 5, color = 'y', label = 'original')
    plt.plot(dateTimeList[:-1], sList, ls = 'None', marker = 'x', ms = 2 , color = 'black', label = 'adjusted')
    plt.xticks([datetime.strptime('2007-09-10 10:00:00', '%Y-%m-%d %H:%M:%S'), 
                datetime.strptime('2007-09-10 15:00:00', '%Y-%m-%d %H:%M:%S'),
                datetime.strptime('2007-09-11 09:30:00', '%Y-%m-%d %H:%M:%S'), 
                datetime.strptime('2007-09-11 15:00:00', '%Y-%m-%d %H:%M:%S')])
    plt.ylim(0,5000)
    plt.title('Original MTW Trade Share VS Adjusted MTW Trade Share')
    plt.xlabel('Time')
    plt.ylabel('Number of Shares')
    plt.legend()
    plt.show()
    
def ori_vs_adj_midQuote_NVDA():
    dayStartNVDA = '20070910' # Start day
    dayEndNVDA = '20070911' # End day
    
    parentddir1 = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    parentddir2 = os.path.abspath(os.path.join(parentddir1, os.path.pardir))
    
    oriQuoteStartNVDA = TAQQuotesReader(os.path.join(parentddir2, 'R/quotes/'+dayStartNVDA+'/NVDA_quotes.binRQ'))
    oriQuoteEndNVDA = TAQQuotesReader(os.path.join(parentddir2, 'R/quotes/'+dayEndNVDA+'/NVDA_quotes.binRQ'))
    
    oriPriceNVDA = [] # List to store price
    oriShareNVDA = [] # List to store number of shares
    timeList = []
    
    # Append data to each of the lists
    for i in range(oriQuoteStartNVDA.getN()):
        oriPriceNVDA.append((oriQuoteStartNVDA.getAskPrice(i) + oriQuoteStartNVDA.getBidPrice(i))/2)
        oriShareNVDA.append((oriQuoteStartNVDA.getAskSize(i) + oriQuoteStartNVDA.getBidSize(i))/2)
        timeList.append(1189396800000 + oriQuoteStartNVDA.getMillisFromMidn(i))   
        
    for i in range(oriQuoteEndNVDA.getN()):
        oriPriceNVDA.append((oriQuoteEndNVDA.getAskPrice(i) + oriQuoteEndNVDA.getBidPrice(i))/2)
        oriShareNVDA.append((oriQuoteEndNVDA.getAskSize(i) + oriQuoteEndNVDA.getBidSize(i))/2)
        timeList.append(1189483200000 + oriQuoteEndNVDA.getMillisFromMidn(i))
    
    dateTimeList = []
    for timeStamp in timeList:
        dateTimeList.append(datetime.fromtimestamp(timeStamp/1000))
    
    adjQuoteStartNVDA = BinReader(os.path.join(os.getcwd(), 'adjusted_quotes/NVDA_quotes.gz'), '>QIIfIf', 100)
    ts0, _, asize0, askp, bsize0, bidp = adjQuoteStartNVDA.next()
    
    ts = []
    ts.append(ts0)
    share = []
    share.append(int((asize0 + bsize0)/2))
    price = []
    price.append((askp+bidp)/2)
    
    while adjQuoteStartNVDA.hasNext():
        t, _, asize, ap, bsize, bp = adjQuoteStartNVDA.next()
        ts.append(t)
        share.append(int((asize+bsize)/2))
        price.append((ap+bp)/2)
    
    sIdx = binarySearch(ts, 0, len(ts)-1, timeList[0])
    eIdx = binarySearch(ts, 0, len(ts)-1, timeList[-1])
    
    pList = price[sIdx:eIdx+1]
    sList = share[sIdx:eIdx+1]
    
    adjQuoteStartNVDA.close()
      
    plt.figure(figsize=(9,6))
    ax = plt.gca()
    xfmt = mdates.DateFormatter('%m-%d %H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(dateTimeList[:-6], oriPriceNVDA[:-6], ls = 'None', marker = 'o', ms = 5, color = 'y', label = 'original')
    plt.plot(dateTimeList[:-6], pList, ls = 'None', marker = 'x', ms = 2 , color = 'black', label = 'adjusted')
    plt.xticks([datetime.strptime('2007-09-10 10:00:00', '%Y-%m-%d %H:%M:%S'), 
                datetime.strptime('2007-09-10 15:00:00', '%Y-%m-%d %H:%M:%S'),
                datetime.strptime('2007-09-11 09:30:00', '%Y-%m-%d %H:%M:%S'), 
                datetime.strptime('2007-09-11 15:00:00', '%Y-%m-%d %H:%M:%S')])
    plt.title('Original NVDA Mid-Quote Price VS Adjusted Mid-Quote NVDA Price')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
     
    plt.figure(figsize=(9,6))
    ax = plt.gca()
    xfmt = mdates.DateFormatter('%m-%d %H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(dateTimeList[:-6], oriShareNVDA[:-6], ls = 'None', marker = 'o', ms = 5, color = 'y', label = 'original')
    plt.plot(dateTimeList[:-6], sList, ls = 'None', marker = 'x', ms = 2 , color = 'black', label = 'adjusted')
    plt.xticks([datetime.strptime('2007-09-10 10:00:00', '%Y-%m-%d %H:%M:%S'), 
                datetime.strptime('2007-09-10 15:00:00', '%Y-%m-%d %H:%M:%S'),
                datetime.strptime('2007-09-11 09:30:00', '%Y-%m-%d %H:%M:%S'), 
                datetime.strptime('2007-09-11 15:00:00', '%Y-%m-%d %H:%M:%S')])
    plt.ylim(0,200)
    plt.title('Original NVDA Mid-Quote Share VS Adjusted NVDA Mid-Quote Share')
    plt.xlabel('Time')
    plt.ylabel('Number of Shares')
    plt.legend()
    plt.show()

def ori_vs_adj_midQuote_MTW():   
    dayStartMTW = '20070910' # Start day
    dayEndMTW = '20070911' # End day
    
    parentddir1 = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    parentddir2 = os.path.abspath(os.path.join(parentddir1, os.path.pardir))
    
    oriQuoteStartMTW = TAQQuotesReader(os.path.join(parentddir2, 'R/quotes/'+dayStartMTW+'/MTW_quotes.binRQ'))
    oriQuoteEndMTW = TAQQuotesReader(os.path.join(parentddir2, 'R/quotes/'+dayEndMTW+'/MTW_quotes.binRQ'))
    
    oriPriceMTW = [] # List to store price
    oriShareMTW = [] # List to store number of shares
    timeList = []
    
    # Append data to each of the lists
    for i in range(oriQuoteStartMTW.getN()):
        oriPriceMTW.append((oriQuoteStartMTW.getAskPrice(i) + oriQuoteStartMTW.getBidPrice(i))/2)
        oriShareMTW.append((oriQuoteStartMTW.getAskSize(i) + oriQuoteStartMTW.getBidSize(i))/2)
        timeList.append(1189396800000 + oriQuoteStartMTW.getMillisFromMidn(i))
        
    for i in range(oriQuoteEndMTW.getN()):
        oriPriceMTW.append((oriQuoteEndMTW.getAskPrice(i) + oriQuoteEndMTW.getBidPrice(i))/2)
        oriShareMTW.append((oriQuoteEndMTW.getAskSize(i) + oriQuoteEndMTW.getBidSize(i))/2)
        timeList.append(1189483200000 + oriQuoteEndMTW.getMillisFromMidn(i))
    
    dateTimeList = []
    for timeStamp in timeList:
        dateTimeList.append(datetime.fromtimestamp(timeStamp/1000))
    
    adjQuoteStartMTW = BinReader(os.path.join(os.getcwd(), 'adjusted_quotes/MTW_quotes.gz'), '>QIIfIf', 100)
    ts0, _, asize0, askp, bsize0, bidp = adjQuoteStartMTW.next()
    
    ts = []
    ts.append(ts0)
    share = []
    share.append(int((asize0 + bsize0)/2))
    price = []
    price.append((askp+bidp)/2)
    
    while adjQuoteStartMTW.hasNext():
        t, _, asize, ap, bsize, bp = adjQuoteStartMTW.next()
        ts.append(t)
        share.append(int((asize+bsize)/2))
        price.append((ap+bp)/2)
    
    sIdx = binarySearch(ts, 0, len(ts)-1, timeList[0])
    eIdx = binarySearch(ts, 0, len(ts)-1, timeList[-1])
    
    pList = price[sIdx:eIdx+1]
    sList = share[sIdx:eIdx+1]
    
    adjQuoteStartMTW.close()
      
    plt.figure(figsize=(9,6))
    ax = plt.gca()
    xfmt = mdates.DateFormatter('%m-%d %H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(dateTimeList[:-6], oriPriceMTW[:-6], ls = 'None', marker = 'o', ms = 5, color = 'y', label = 'original')
    plt.plot(dateTimeList[:-6], pList, ls = 'None', marker = 'x', ms = 2 , color = 'black', label = 'adjusted')
    plt.xticks([datetime.strptime('2007-09-10 10:00:00', '%Y-%m-%d %H:%M:%S'), 
                datetime.strptime('2007-09-10 15:00:00', '%Y-%m-%d %H:%M:%S'),
                datetime.strptime('2007-09-11 09:30:00', '%Y-%m-%d %H:%M:%S'), 
                datetime.strptime('2007-09-11 15:00:00', '%Y-%m-%d %H:%M:%S')])
    plt.title('Original MTW Mid-Quote Price VS Adjusted MTW Mid-Quote Price')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
     
    plt.figure(figsize=(9,6))
    ax = plt.gca()
    xfmt = mdates.DateFormatter('%m-%d %H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(dateTimeList[:-6], oriShareMTW[:-6], ls = 'None', marker = 'o', ms = 5, color = 'y', label = 'original')
    plt.plot(dateTimeList[:-6], sList, ls = 'None', marker = 'x', ms = 2 , color = 'black', label = 'adjusted')
    plt.xticks([datetime.strptime('2007-09-10 10:00:00', '%Y-%m-%d %H:%M:%S'), 
                datetime.strptime('2007-09-10 15:00:00', '%Y-%m-%d %H:%M:%S'),
                datetime.strptime('2007-09-11 09:30:00', '%Y-%m-%d %H:%M:%S'), 
                datetime.strptime('2007-09-11 15:00:00', '%Y-%m-%d %H:%M:%S')])
    plt.ylim(0,200)
    plt.title('Original MTW Mid-Quote Share VS Adjusted MTW Mid-Quote Share')
    plt.xlabel('Time')
    plt.ylabel('Number of Shares')
    plt.legend()
    plt.show()

def binarySearch(arr, start, end, key): 
  
    # Check base case 
    if end >= start: 
  
        mid = start + int((end - start)/2)
  
        # If element is present at the middle itself 
        if arr[mid] == key: 
            return mid 
          
        # If element is smaller than mid, then it can only 
        # be present in left subarray 
        elif arr[mid] > key: 
            return binarySearch(arr, start, mid-1, key) 
  
        # Else the element can only be present in right subarray 
        else: 
            return binarySearch(arr, mid+1, end, key) 
  
    else: 
        # Element is not present in the array 
        return -1 

if plot == True:  
    ori_vs_adj_trade_NVDA()
    ori_vs_adj_trade_MTW()
    ori_vs_adj_midQuote_NVDA()
    ori_vs_adj_midQuote_MTW()