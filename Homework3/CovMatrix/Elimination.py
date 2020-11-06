'''
Created on Mar 8, 2020

@author: Zibin
'''

import os
import holidays
import json
from LeeCode.BinReader import BinReader
from datetime import datetime
from datetime import timedelta

parentDir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)) 
quotePath = parentDir + '/clean_quotes/'
tradePath = parentDir + '/clean_trades/'

def dateTrade(startDate = datetime(2007, 6, 20), endDate = datetime(2007, 9, 21)):    
    '''function to get a list of trading day during the period'''  
    
    usHoliday = holidays.US() # Get the holidays in US
    dateList = []
        
    for i in range(int((endDate - startDate).days)):
        nextDate = startDate + timedelta(i)
        # Check if the day is a business day
        if nextDate.weekday() not in (5, 6) and nextDate not in usHoliday:
            tradeDay = nextDate.strftime('%Y%m%d')
            dateList.append(tradeDay)
            
    return dateList

def sliceTS(ts):
    ''' function to slice time stamps '''
    
    sliceIdx = [0] # list to store the start index of each day
    sevenHour = 7 * 60 * 60 * 1000 # to pass one trading day
    idx = 0
    startTS = ts[0]           
       
    while True:
        
        while ts[idx] < startTS + sevenHour and idx < len(ts)-1:
            idx += 1 # increase until the end of this day
            
        sliceIdx.append(idx) # start of the next day
        
        if idx < len(ts)-1:   
            startTS = ts[idx+1] # move the start point to the next day
        else:
            break
        
    return sliceIdx 

def eliminateStock():
    defectDic = {}
    dateList = dateTrade()   
    count = 0
    
    for filename in sorted(os.listdir(quotePath)): 
        if filename.endswith('.gz'):
            count += 1
            print('processing ' + filename[:-10] + ' -- Stock #' +str(count))
            path = quotePath + filename
            reader = BinReader(path, '>QIIfIf', 100)
            ts = []
            si = []
            pr = []
            while reader.hasNext():
                d = reader.next()
                ts.append(d[0])
                si.append(int((d[2]+d[4])/2))
                pr.append((d[3]+d[5])/2)
              
            reader.close()
                     
            sliceIdx = sliceTS(ts) 
            # print(sliceIdx)
            # print(filename[:-3], 'has day:', len(sliceIdx)) 
            if len(sliceIdx) < 66 :
                #print(filename[:-10] + ' is defective')
                date = []
                for idx in sliceIdx:
                    num = ts[idx]/1000
                    time = datetime.fromtimestamp(num).date()
                    date.append(time.strftime('%Y%m%d'))
      
                set1 = set(date)
                set2 = set(dateList)
                missing = list(sorted(set2 - set1))
                # Adding a new key value pair
                defectDic.update({filename[:-10] : missing})
                print(defectDic)
              
            else:
                # print(filename[:-10] + ' is good')
                pass
           
    for filename in sorted(os.listdir(tradePath)): 
        if filename.endswith('.gz'):
            count += 1
            print(filename[:-10] + ' -- Stock #'+str(count))
            path = tradePath + filename
            reader = BinReader(path, '>QIIf', 100)
            ts = []
            si = []
            pr = []
            while reader.hasNext():
                d = reader.next()
                ts.append(d[0])
                si.append(d[2])
                pr.append(d[3])
             
            reader.close()
                    
            sliceIdx = sliceTS(ts) 
            # print(sliceIdx)
            # print(filename[:-3], 'has day:', len(sliceIdx)) 
            if len(sliceIdx) < 66:
                #print(filename[:-10] + ' is defective')
                date = []
                for idx in sliceIdx:
                    num = ts[idx]/1000
                    time = datetime.fromtimestamp(num).date()
                    date.append(time.strftime('%Y%m%d'))
     
                set1 = set(date)
                set2 = set(dateList)
                missing = list(sorted(set2 - set1))
                # Adding a new key value pair
                defectDic.update({filename[:-10] : missing})
                print(defectDic)
             
            else:
                # print(filename[:-10] + ' is good')
                pass
    
    with open('defectStock.txt', 'w') as file:
        file.write(json.dumps(defectDic)) 
    print('Done')          
    return defectDic

def deleteFile():
    dic = eliminateStock() # dictionary of defected stocks
    r = list(dic.keys()) # list contained all tickers of defected stocks
    
    # r = ['NE','COV','EXPE','TEL','MKC','OMC','SUNW','DFS','MTW','JAVA','MXM','ABC','RTN','AGN']
    # Code to eliminate stocks  
    for filename in os.listdir(quotePath):
        path = quotePath + filename
        for ticker in r:
            if ticker + '_quotes.gz' in filename:
                os.remove(path)
                  
    for filename in os.listdir(tradePath):
        path = tradePath + filename
        for ticker in r:
            if ticker + '_trades.gz' in filename:
                os.remove(path)
                
    return r