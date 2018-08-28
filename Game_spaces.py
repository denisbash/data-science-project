# -*- coding: utf-8 -*-
"""
Imports custom module Game which contains the most complete information
about shots for those games (about 85 percent) for which exception due to
defiency in the data was not raised.

The second imported custom module 'xDict' contains the definition of
a custom dictionary class xDict as the built-in dictionary class does not 
support addition/increment operation we needed.
"""


from collections import Counter
from copy import deepcopy
import os

os.chdir('C:/Users/Owner/Anaconda3/New folder')

import Game
import xDict

class Game_Spaces:
    
    def __init__(self, name=None, shot_types=('B','M','S','G','N')):
        """ Example of a name: 2017030415.
        This class is for collecting complete statistics about shots
        viewed as letters of 'words'.
        
        """
        self.activation=0
        self.x=[{},{}]
        self.T=[[0,0],[0,0]]
        self.spaces=[{},{}]
        self.Dict=self.spaces
        self.Attack=[{key:0 for key in shot_types},{key:0 for key in shot_types}]        
        self.elem_types=('B','M','S','G','N')
        self.s_types={}
        temp_str=''
        for item in shot_types:
            self.s_types[item]={}
            temp_str+=item
        sits=('B', 'M', 'S', 'G', 'N')
        self.elementary_types=[]
        for elem in sits:
            if elem in temp_str:
                self.elementary_types.append(elem)
        for i in range(2):
            self.Dict[i]['Start']=Counter()
            for elem in self.elementary_types:
                self.x[i][('Start', elem)]=xDict.xDict()
                self.Dict[i][elem]=Counter()                
                for el in self.elementary_types:
                    self.x[i][(elem, el)]=xDict.xDict()
        if name is not None:
            self.game=Game.Game(name).Game
            self.game_spaces()
            self.activation=1
            

    def game_spaces(self):
        for i in range(2):              
            Temp={}
            Temp['Start']=[]
            temp=Temp['Start']
            str_temp='Start'
            for item in self.elementary_types:
                Temp[item]=[]
            t_0=0
            T=self.game[i][-1][0]            
            t_p=t_0
            
            for item in self.game[i]:                               
                t_c=item[0]
                temp.append(t_c-t_p) 
                self.x[i][(str_temp, item[3])].app(t_c-t_p, abs(item[1]), abs(item[2]), item[4])                   
                t_p=t_c
                
                if item[3] in self.elementary_types:
                    temp=Temp[item[3]]
                    str_temp=item[3]
                    self.Attack[i][item[3]]+=1
                else:
                    temp=[]
            self.T[i]=[T, len(self.game[i])]
            self.Dict[i]['Start']=Counter(Temp['Start'])
            for item in self.elementary_types:
                Temp[item].sort()
                self.Dict[i][item]=Counter(Temp[item])
                
    def get_prob(self, typ=0):        
        N_w=[self.T[0][1], self.T[1][1]]
        self.prob_0=[deepcopy(self.Dict[0]['Start']),deepcopy(self.Dict[1]['Start'])]
        self.prob_1=deepcopy(self.Dict)
        self.prob_2=deepcopy(self.x)
        temp_dict={0:self.prob_0, 1:self.prob_1, 2:self.prob_2}        
        for i in range(2):            
            for key in self.prob_1[i]['Start'].keys():
                self.prob_1[i]['Start'][key]=self.prob_1[i]['Start'][key]/N_w[i]
                
            for item in self.elementary_types:
                self.Attack[i][item]=self.Attack[i][item]/self.activation                
                self.prob_0[i]+=self.Dict[i][item]
                for key in self.prob_1[i][item].keys():
                    self.prob_1[i][item][key]=self.prob_1[i][item][key]/N_w[i]
                self.prob_2[i][('Start', item)].prob(N_w[i])                
                for it in self.elementary_types:                    
                    self.prob_2[i][(item, it)].prob(N_w[i])
            for key in self.prob_0[i].keys():
                self.prob_0[i][key]=self.prob_0[i][key]/N_w[i]
            
        return temp_dict[typ]
    
    def __iadd__(self, other): 
        self.activation+=other.activation
        for i in range(2):
            for k in range(2):
                self.T[i][k]+=other.T[i][k]
            for item in self.elementary_types:
                self.Attack[i][item]+=other.Attack[i][item]
                self.Dict[i][item]+=other.Dict[i][item]                
                self.x[i][('Start', item)]+=other.x[i][('Start', item)]
                for it in self.elementary_types:
                    self.x[i][(item, it)]+=other.x[i][(item, it)]                    
            self.Dict[i]['Start']+=other.spaces[i]['Start']
            
        return self
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                