'''
Created on Feb 25, 2020

@author: Nate, Zibin, Martin
'''

from PartB.ReturnComputer import Computer
import matplotlib.pyplot as plt
import os
import numpy as np

''' Plot different x-interval returns before and after clean '''

plot = False # Change to True if want to plot

parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
path1 = parentddir + '/PartA/adjusted_trades/AYE_trades.gz'
path2 = parentddir + '/clean_trades/AYE_trades.gz'

adjAYE = Computer(path1, 'trades')
cleAYE = Computer(path2, 'trades')

s10 = adjAYE.computeReturn(1/6) # 10 seconds return
s30 = adjAYE.computeReturn(1/2) # 30 seconds return
m1 = adjAYE.computeReturn(1) # 1 minute return
m5 = adjAYE.computeReturn(5) # 5 minutes return
m10 = adjAYE.computeReturn(10) # 10 minutes return
m30 = adjAYE.computeReturn(30) # 30 minutes return
ss10 = cleAYE.computeReturn(1/6)
ss30 = cleAYE.computeReturn(1/2)
mm1 = cleAYE.computeReturn(1)
mm5 = cleAYE.computeReturn(5)
mm10 = cleAYE.computeReturn(10)
mm30 = cleAYE.computeReturn(30)

if plot == True:
    plt.title('10 seconds return before and after clean')
    plt.plot(np.arange(len(m30)), s10[:len(m30)], label = 'before')
    plt.plot(np.arange(len(m30)), ss10[:len(m30)], label = 'after')
    plt.legend()
    plt.show()
    
    plt.title('30 seconds return before and after clean')
    plt.plot(np.arange(len(m30)), s30[:len(m30)], label = 'before')
    plt.plot(np.arange(len(mm30)), ss30[:len(mm30)], label = 'after')
    plt.legend()
    plt.show()
    
    plt.title('1 minute return before and after clean')
    plt.plot(np.arange(len(m30)), m1[:len(m30)], label = 'before')
    plt.plot(np.arange(len(mm30)), mm1[:len(mm30)], label = 'after')
    plt.legend()
    plt.show()
    
    plt.title('5 minutes return before and after clean')
    plt.plot(np.arange(len(m30)), m5[:len(m30)], label = 'before')
    plt.plot(np.arange(len(mm30)), mm5[:len(mm30)], label = 'after')
    plt.legend()
    plt.show()
    
    plt.title('10 minutes return before and after clean')
    plt.plot(np.arange(len(m30)), m10[:len(m30)], label = 'before')
    plt.plot(np.arange(len(mm30)), mm10[:len(mm30)], label = 'after')
    plt.legend()
    plt.show()
    
    plt.title('30 minutes return before and after clean')
    plt.plot(np.arange(len(m30)), m30, label = 'before')
    plt.plot(np.arange(len(mm30)), mm30, label = 'after')
    plt.legend()
    plt.show()