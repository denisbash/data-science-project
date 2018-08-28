# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 23:58:38 2018

@author: Owner
"""

class xDict:
    def __init__(self):
        self.D={}
        
    def app(self, dt, x, y, num):
        if dt in self.D.keys():
            self.D[dt][0]+=x
            self.D[dt][1]+=y
            self.D[dt][2]+=num
            self.D[dt][3]+=1
        else:
            self.D[dt]=[x, y, num,1]
            
    def divide(self, N):
        for dt in self.D.keys():
            self.D[dt][3]=self.D[dt][3]/N
        
            
    def average(self):
        for dt in self.D.keys():
            temp_denomenator=self.D[dt][-1]
            for i in range(len(self.D[dt])-1):
                self.D[dt][i]=self.D[dt][i]/temp_denomenator
                
    def prob(self, N):
        self.average()
        self.divide(N)            
            
    def __iadd__(self, other):
        for dt in other.D.keys():
            if dt in self.D.keys():
                self.D[dt][0]+=other.D[dt][0]
                self.D[dt][1]+=other.D[dt][1]
                self.D[dt][2]+=other.D[dt][2]
                self.D[dt][3]+=other.D[dt][3]
            else:
                self.D[dt]=[other.D[dt][0], other.D[dt][1], other.D[dt][2], other.D[dt][3]]
               
        return self
    