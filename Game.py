# -*- coding: utf-8 -*-
"""
This module contains the definition of the class 'Game' which is the basic
class in our analysis. It contains the complete information about
shots in a particular game.
The information comes from two json files: one with shots' 
coordinates and time,  the other with their descriptions.
They were downloaded by scripts 'playoff.py' and 'regseasons.py'
from the website 'hockeystats.ca'.

The second class defined in this module, 'Chrono_Game' is not used in our
analysis and is only for visualization of the game. However, it can be 
used in further research, and was written with the idea of employing it for
 analysis of games' time evolution.

"""
import json

class Game:
    
    def __init__(self, number):        
        self.Game=self.game(number) 
                  
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
		
    def merge(self, number):
        c=self.load('chart', number)
        s=self.load('shots', number)        
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
                    c_list.append([num,(item.get('x')-c[i][0].get('x'))//1000])
                    
            if len(c_list)==len(s[i]):
                temp=[]
                for k in range(len(c_list)):
                    l=[c_list[k], s[i][k]]
                    temp.append(l)
                game.append(temp)
            else:
                raise Exception                
        return game
                
    def game(self, number):
        scheme=self.merge(number)
        game_scheme=[]
        for i in range(2):
            
            features=[]
            for k in range(len(scheme[i])):
                name=scheme[i][k][1].get('name')
                feature=[]
                feature.append(scheme[i][k][0][1])
                feature.append(scheme[i][k][1].get('x'))
                feature.append(scheme[i][k][1].get('y'))
                if 'blocked' in name:
                    feature.append('B')
                elif 'saved' in name:
                    feature.append('S')
                elif 'Net' in name or 'Goalpost' in name or 'Crossbar' in name:
                    feature.append('M')
                elif scheme[i][k][1].get('color'):
                    feature.append('G')
                else:
                    print('Cannot classify event: ', scheme[i][k])
                    feature.append('N')
                
                feature.append(scheme[i][k][0][0])
                
                features.append(feature)
            game_scheme.append(features)
            
        return game_scheme
                
from operator import itemgetter
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Chrono_Game(Game):    
    def __init__(self, number):        
        super().__init__(number)        
        self.ch_game=self.chrono_game()
        self.s=[]
        self.t=[]
        self.x=[]
        self.y=[]
        self.n=[]
        for item in self.ch_game:
            self.t.append(item[0])
            self.x.append(item[1])
            self.y.append(item[2])
            self.s.append(item[3])
            self.n.append(item[4])
                  
   
                    
    def chrono_game(self):
        def rotate(lst,tm):
            if tm<0:
                lst[4]=-lst[4]
            if lst[1]*tm<0:
                lst[1]=-lst[1]
                lst[2]=-lst[2]
            return lst
        temp_A=[rotate(L,1) for L in self.Game[0]]
        temp_H=[rotate(L,-1) for L in self.Game[1]]
        
        pre_chrono=temp_A+temp_H        
        return sorted(pre_chrono, key=itemgetter(0))
    
    def visualize(self, plot=False):
        fig=plt.figure()
        ax=fig.add_subplot('111', projection='3d')
        cols=[]
        power=[]
        D={'B':'blue','S':'green','M':'yellow','G':'red','N':'black'}
        cols=[D[item] for item in self.s]    
                
        for item_n, item_x in zip(self.n, self.x):
            if item_x>0:
                power.append(50*2**item_n)
            else:
                power.append(50*2**(-item_n))
                
        if plot:
            ax.plot3D(self.x,self.y,self.t)
        else:
            ax.scatter(self.x, self.y, self.t, c=cols, s=power)
            ax.legend(loc='upper right', shadow=True, fontsize='x-large')
         