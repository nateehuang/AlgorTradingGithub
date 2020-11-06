'''
Created on Feb 24, 2020

@author: natehuang
'''
from dbReaders.BinReader import BinReader
import matplotlib.pyplot as plt
import os
from datetime import datetime



if __name__ == '__main__':
    
    # change tick1 for another stock
    tick1 = "RRC"
    filePath = os.path.join(os.getcwd(), "adjusted_trades", tick1+"_trades.gz")
    tr = BinReader(filePath, '>QIIf', 100)
    ts1 = []
    ps1 = []
    while tr.hasNext():
        now = tr.next()
        ts1.append(datetime.fromtimestamp(now[0]/1000))
        ps1.append(now[3])
    
    filePath = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), "clean_trades", tick1+"_trades.gz")
    tr = BinReader(filePath, '>QIIf', 100)
    ts2 = []
    ps2 = []
    while tr.hasNext():
        now = tr.next()
        ts2.append(datetime.fromtimestamp(now[0]/1000))
        ps2.append(now[3])
        
    print("Plot trades")
    plt.figure(figsize=(12,9))
    plt.plot(ts1, ps1, label = "before clean")
    plt.plot(ts2, ps2, label = "after clean")
    plt.ylabel("Price")
    plt.xlabel("Time Stamp")
    plt.legend(loc="upper right")
    plt.title(tick1+" Trade data Before clean and after clean")
    plt.savefig(tick1+"_trades.png")
    
    # change tick1 for another stock
    filePath = os.path.join(os.getcwd(), "adjusted_quotes", tick1+"_quotes.gz")
    tr = BinReader(filePath, '>QIIfIf', 100)
    ts1 = []
    ps1 = []
    while tr.hasNext():
        now = tr.next()
        ts1.append(datetime.fromtimestamp(now[0]/1000))
        ps1.append((now[3]+now[5])/2)
    
    filePath = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), "clean_quotes", tick1+"_quotes.gz")
    tr = BinReader(filePath, '>QIIfIf', 100)
    ts2 = []
    ps2 = []
    while tr.hasNext():
        now = tr.next()
        ts2.append(datetime.fromtimestamp(now[0]/1000))
        ps2.append((now[3]+now[5])/2)
        
    print("Plot quotes")
    plt.figure(figsize=(12,9))
    plt.plot(ts1, ps1, label = "before clean")
    plt.plot(ts2, ps2, label = "after clean")
    plt.ylabel("Mid Price")
    plt.xlabel("Time Stamp")
    plt.legend(loc="upper right")
    plt.title(tick1+" Quotes data Before clean and after clean")
    plt.savefig(tick1+"_quotes.png")
    print("Done")