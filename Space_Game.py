# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 02:47:09 2018

@author: Owner
"""
from collections import Counter
import json
import copy

class Space_Game:
    
    def __init__(self, number=None): 
        """ Here we used only one of the json files to extract information --
        we ignore shots' positions."""
        self.Game=[[],[]]
        self.Dict=[{},{}]        
        self.elem_types=(-2,-1,0,1,2)        
        for i in range(2):
            for num in self.elem_types:
                self.Dict[i][num]=Counter()            
        self.T=[[0,0],[0,0]]
        if number is not None:
            self.Game=self.s_game(number)
            self.spaces()
                   
    def load(self, tp, game):        
        if game[5]=='2':
            dirs='Regular'+game[2:4]
        elif game[5]=='3':
            dirs='Playoff'+game[2:4]
        else:
            print('No such game')
            return []
        root='C:/Users/Owner/Documents/Hockey/'
        try:
            f=open(root+dirs+'/'+game+'/'+tp+game+'.txt', 'r')
            jf=json.load(f)
                      
        except Exception as e:
            self.trans=[]
            print(dirs+'/'+game)
        finally:
            if f:
                f.close()
        return jf
		
    def s_game(self, number):
        c=self.load('chart', number)        
        game=[]        
        for i in range(2):
            count=0
            c_list=[]
            for item in c[i]:
                if item.get('y')==count+1:
                    count+=1
                    name=item.get('name')
                    if '5v3' in name:
                        num=2
                    elif '5v4' in name:
                        num=1
                    elif '4v5' in name:
                        num=-1
                    elif '3v5' in name:
                        num=-2
                    else:
                        num=0
                    c_list.append(((item.get('x')-c[i][0].get('x'))//1000, num))
            game.append(c_list)                
        return game
                
    def spaces(self):
        for i in range(2):
            temp={-2:[],-1:[],0:[],1:[],2:[]}
            t_0=0
            T=self.Game[i][-1][0]            
            t_p=t_0            
            for item in self.Game[i]:                               
                t_c=item[0]
                temp[item[1]].append(t_c-t_p) 
                t_p=t_c                
            self.T[i]=[T, len(self.Game[i])]            
            for num in range(-2,3):
                temp[num].sort()
                self.Dict[i][num]=Counter(temp[num])
            
            
    def get_prob(self, typ=0):
        self.prob_0=[Counter(),Counter()]
        self.prob_1=copy.deepcopy(self.Dict)
        for i in range(2):
            for num in self.prob_1[i].keys():
                self.prob_0[i]+=self.prob_1[i][num]
                for counter_key in self.prob_1[i][num].keys():
                    self.prob_1[i][num][counter_key]=self.prob_1[i][num][counter_key]/self.T[i][1]
            for key in self.prob_0[i].keys():
                self.prob_0[i][key]=self.prob_0[i][key]/self.T[i][1]
        D_return={0:self.prob_0, 1:self.prob_1}
        return D_return[typ]
        
        
                
    def __iadd__(self, other):  
        '''For a time being, leave self.Game intact-later could concatenate'''
        
        for i in range(2):
            for k in range(2):
                self.T[i][k]+=other.T[i][k]
            for num in range(-2,3):
                self.Dict[i][num]+=other.Dict[i][num]                
        return self
                
            
        