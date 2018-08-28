# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 12:18:07 2018

@author: Owner
"""
import Game
import matplotlib.pyplot as plt
from collections import Counter


class Shots():
    Lx=90
    Ly=40
    def __init__(self, name=None, N_xfg=10, N_yfg=10):
        self.N_xfg=N_xfg
        self.N_yfg=N_yfg
        self.x_range=round(Shots.Lx/self.N_xfg)
        self.y_range=round(Shots.Ly/self.N_yfg)
        self.Shots_dict=[{},{}]
        self.Shots_params=('T','X','Y','F','N')
        self.bins_cg=[Counter(),Counter()] 
        self.feature=[[],[]]
        self.Features=[[],[]]
        for i in range(2):
            for s in self.Shots_params:
                self.Shots_dict[i][s]=[]
            self.Shots_dict[i]['V']=[]
        if name is None:
            self.Away=[]
            self.Home=[]
            self.number=0
        else:
            self.Game=Game.Game(name)
            self.Away=self.Game.Game[0]
            self.Home=self.Game.Game[1]
            self.number=1
            self.coarse_grain()
                             
        for item in self.Away:
            for k in range(5):
                self.Shots_dict[0][self.Shots_params[k]].append(item[k])
        self.Shots_dict[0]['V']=list(zip(self.Shots_dict[0]['X'],self.Shots_dict[0]['Y']))
        for item in self.Home:
            for k in range(5):
                self.Shots_dict[1][self.Shots_params[k]].append(item[k])
        self.Shots_dict[1]['V']=list(zip(self.Shots_dict[1]['X'],self.Shots_dict[1]['Y']))
        self.coarse_grain()
        self.featurize() 
        if self.number:
            for i in range(2):                
                self.Features[i].append(self.feature[i])      
               
    def coarse_grain(self):
        N_xfg=self.N_xfg
        N_yfg=self.N_yfg
        def F(x):
            if x[0]<0:
                x=[-x[0],-x[1]]
            return x
        self.V_cg=[]
        for i in range(2):
            self.V_cg.append([(round(F(s)[0]/N_xfg),round(F(s)[1]/N_yfg)) for s in self.Shots_dict[i]['V']])
        self.bins_cg=[Counter(self.V_cg[0]),Counter(self.V_cg[1])]
                
    def visualize(self, grain=True, prob=True):
        Func=lambda x: list(zip(*x))        
        D={True:self.V_cg, False:[self.Shots_dict[0]['V'],self.Shots_dict[1]['V']]}
        if prob:
            self.get_prob()
            key_range=self.key_range(3)
            
            X=[]
            Y=[]
            Z=[]
            for key in key_range:
                Z.append(self.prob_cg[0][key])
                X.append(key[0])
                Y.append(key[1])
            fig=plt.figure()                       
            ax=fig.add_subplot('111', projection='3d')
            ax.scatter(X,Y,Z,c='red')
            
        fig, axes=plt.subplots(2,1, figsize=(10,10))
        for i in range(2):
            axes[i].scatter(Func(D[grain][i])[0], Func(D[grain][i])[1])
            
    def featurize(self):        
        for i in range(2):
            temp=[]            
            for x in range(2,self.x_range+1):
                for y in range(-self.y_range,self.y_range+1):
                    temp.append(self.bins_cg[i][(x,y)])
            self.feature[i]=temp
           
    
    def get_prob(self):
        self.prob_cg=[Counter(),Counter()]
        self.Norm_factor=self.x_range*self.y_range*2*self.number
        for i in range(2):
            for key in self.bins_cg[i].keys():
                self.prob_cg[i][key]=self.bins_cg[i][key]/self.Norm_factor
        return [self.prob_cg[0],self.prob_cg[1]]
    
    def key_range(self):
        temp=[]
        for x in range(self.x_range+1):
            for y in range(-self.y_range,self.y_range+1):
                temp.append((x,y))
        return temp
    
    def key_index(self,tup):
        index=-1        
        for x in range(self.x_range+1):
            for y in range(-self.y_range,self.y_range+1):
                index+=1
                if (x,y)==tup:
                    return index
        return None
        
        
            
    def __iadd__(self, other):
        for i in range(2):
            self.Shots_dict[i]['V']+=other.Shots_dict[i]['V']
            self.bins_cg[i]+=other.bins_cg[i]
            self.V_cg[i]+=other.V_cg[i]
            if other.number:
                self.Features[i].append(other.feature[i])
            for key in self.Shots_params:
                self.Shots_dict[i][key]+=other.Shots_dict[i][key]
            self.number+=other.number
            
            #self.feature=
        return self
            




































