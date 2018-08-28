# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 03:56:00 2018

@author: Owner
This module contains the definition of a class 'Word_Game' which
extracts independent words from a game represented by an instance of 
the class 'Space_Game', counts them and keeps them in a Counter.
Independent words are substrings of consequative letters in the game 
viewed as text, which start and end with the letter '1', and are preceeded 
and followed by time intervals without attacks (zeroes) longer than 
the correlation length, set by default to 30 (seconds).     
"""
import os
os.chdir('C:/Users/Owner/Anaconda3/New folder')
import Space_Game
from collections import Counter
import pickle
import operator
import copy
'''def ind_words(N):
    root='C:/Users/Owner/Documents/Hockey'
    games_list=[]
    for dirs in os.listdir(root):
        games_list+=os.listdir(root+'/'+dirs)
    Stat_A=Counter()
    Stat_H=Counter()
    for gm in games_list:
        temp=game(gm,N)
        Stat_A+=temp[0]
        Stat_H+=temp[1]    
    Stat=(Stat_A, Stat_H)
    f=open('Ind_Words'+str(N), 'wb')
    pickle.dump(Stat, f)
    f.close()
    return Stat'''
    
class Word_Game():
            
    def __init__(self,name=None, N=30):        
        """Keyword args: name=None, N=30 (correlation length in seconds)."""        
        L=[[],[]]
        self.C=[Counter(),Counter()]
        self.N=[0,0]
        self.elem_types=('single',)
        self.Dict=[{'single':self.C[0]},{'single':self.C[1]}]
        if name is not None:
            Game=Space_Game.Space_Game(name).Game
            for team in range(2):
                end_index=len(Game[team])
                index=0        
                buffer=[]
                while index<end_index:            
                    t_cur=Game[team][index][0]
                    try:                
                        t_next=Game[team][index+1][0]
                    except Exception:
                        t_next=t_cur+N
                    if t_next<t_cur+N:
                        buffer.append(t_next-t_cur)                       
                    else:
                        L[team].append(tuple(buffer)) # to make arg of Counter hashable
                        self.N[team]+=len(buffer)+1
                        buffer=[]
                    index+=1                
                self.C[team]+=Counter(L[team])
    def get_prob(self):
        """Returns [Away prob Counter, Home prob Counter]."""
        self.prob=copy.deepcopy(self.C)
        for i in range(2):
            for key in self.prob[i].keys():
                self.prob[i][key]=self.prob[i][key]/self.N[i]
        return self.prob
                        
    def sort(self, stat, N=60):
        """ Sorts and returns N first tuples of (word, Counter)."""
        assert type(stat) is list and len(stat)==2
        
        away=sorted(stat[0].items(), key=operator.itemgetter(1)) 
        home=sorted(stat[1].items(), key=operator.itemgetter(1))
        return [away[:N], home[:N]]
    
    def __iadd__(self, other):
        for i in range(2):
            self.C[i]+=other.C[i]
            self.N[i]+=other.N[i]
        return self
            
    def __add__(self, other):
        Temp=copy.deepcopy(self)        
        Temp+=other
        return Temp
    
    def __radd__(self, other):
        return self.__add__(other)
    
    