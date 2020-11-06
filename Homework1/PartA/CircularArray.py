'''
Created on Feb 23, 2020

@author: natehuang
'''
import numpy as np

class CircularArray(object):
    '''
    classdocs
    '''


    def __init__(self, size):
        '''
        Constructor
        '''
        self._size = size
        self._arr = np.array([0.]*size)
        self._next = 0
        self._oldest = 0.
        self._sum = 0.
        self._sumXX = 0.
    
    def index(self, n):
        return n % self._size
    
    def add(self, p):
        self._oldest = self.get(self._next)
        self._sum -= self._oldest
        self._sumXX -= self._oldest**2

        self.set(self._next, p)
        self._sum += p

        self._sumXX += p**2
        self._next += 1
    
    def set(self, i, p):
        self._arr[self.index(i)] = p
        
    def get(self, i):
        return self._arr[self.index(i)]
        
    def mean(self):    
        return self._sum/self._size
    
    def std(self):
        diffOfSums = (self._sumXX-self._sum*self._sum/self._size)
        return np.sqrt(diffOfSums/(self._size-1))
        
        
    
        