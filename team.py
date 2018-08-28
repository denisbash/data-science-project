# -*- coding: utf-8 -*-
"""
The main module. Contains definition of classes 'Team'and its derivatives
'WTeam' (and its derivatives 'SubWTeam' and 'RandSubWTeam') and 'STeam'.
Imports all four representations of games defined in modules 'Game_spaces',
'Space_Game', 'independent_words' and 'Shots'.
  'Game_spaces' contains the most complete representation of a game -- 
the complete information about all shots, but cannot be initialized for about 
15 percent of the games due to defects in the data from hockeystats.ca --
Exception is raised in those cases. They are caught during initialization of
'Team' and 'defective' games' names are placed in a list self.Exc_list.
  'Space_Game' discards the information about shots' positions to include the
remaining 15 percent of the games.
  'independent_words' ignores information about shots' positions and has
 more carefull treatement of words taking into account correlation length of
games.
  'Shots' ignores all information about a game except shots' coordinates.
  
'Team' is initialized with the team's standard abbreviation, f.e., 'MTL'
for Montreal Canadians or 'WSH' for Washington Capitals. With the name as a
key, previously created and saved in json dictionary objects are searched 
for the list of games' names which are then used to instantiate Game objects
of the chose kind.
They are put in dictionaries.

When probabilities are needed to be computed to get feature vectors, 
the function 'group_stat' from module 'group_stat' is called which computes 
these probabilities.
  
To view multiple teams' feature vectors on plots, one initializes each of them,
calls on each the method self.featurize_team(N), then sums and calls 
self.features3D(...) for the sum.

Example: 'MTL' and 'WSH'.

m=team.WTeam('MTL'), w=team.Wteam('WSH')
m.featurize_team(60), w.featurize_team(60)
T=m+w
T.features3D(0,1,2)
  
In the end, we used only about 20-30 percent of the developed code 
(we didn't use anything related to shots coordinates, and essentially 
used only a small part of 'Game_spaces') as we started seeing interesting 
things with a small part of the total data. The unused code can be employed 
for further research in this area as we only saw the tip of an iceberg.

"""
import json
import random
import Game_spaces
import Space_Game
import independent_words as i_w
import Shots
import group_stat
import matplotlib.pyplot as plt
import operator
from math import log
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from collections import Counter
from copy import deepcopy
from mpl_toolkits.mplot3d import Axes3D


class Team():
    Game_kind={0:Game_spaces.Game_Spaces, 1:Space_Game.Space_Game, 
               2:i_w.Word_Game, 3:Shots.Shots}
    def __init__(self, team=None, kind=0):
        self.A_dict={}
        self.H_dict={}
        self.Exc_list=[[],[]]        
        self.name=''
        self.kind=kind  
        self.feature_map=[{},{}]
        if team is not None:
            self.name=team
            fa=open('C:/Users/Owner/Anaconda3/New folder/Away_dict.txt', 'rt')
            fh=open('C:/Users/Owner/Anaconda3/New folder/Home_dict.txt', 'rt')
            at=json.load(fa)
            ht=json.load(fh)
            fa.close()
            fh.close()
            la=[]
            lh=[]
            self.Away_opponents=at[self.name]
            self.Home_opponents=ht[self.name]
            for x in at[self.name].keys():
                la+=at[self.name][x]
            LA=[]
            for x in ht[self.name].keys():
                lh+=ht[self.name][x]
            LH=[]
            for item in la:
                try:
                    self.A_dict[item]=Team.Game_kind[kind](item)
                    LA.append(item)
                except Exception:
                    self.Exc_list[0].append(item)                    
            for item in lh:
                try:
                    self.H_dict[item]=Team.Game_kind[kind](item)
                    LH.append(item)
                except Exception:
                    self.Exc_list[1].append(item)
            LA.sort()
            LH.sort()
            self.LA=LA
            self.LH=LH
            
                    
    def dict_update(self, other):
        self.A_dict.update(other.A_dict)
        self.H_dict.update(other.H_dict) 
        
    def get_prob(self):
        try:            
            self.A_prob=group_stat.group_stat(self.A_dict)[0]            
        except group_stat.GetProbException as ex:
            self.A_prob=ex.temp[0]            
            self.Attack_Away=ex.Attack
            self.games_away=ex.activation
        try:
            self.H_prob=group_stat.group_stat(self.H_dict)[1]
        except group_stat.GetProbException as ex:
            self.H_prob=ex.temp[1]            
            self.Attack_Home=ex.Attack
            self.games_home=ex.activation            
        self.prob=True
    
    def feature_prob(self,N=10):
        self.get_prob()
        key_range={0:lambda x:range(x), 1:lambda x:range(x), 
                   2:lambda x:[()]+[(i,) for i in range(x-1)], 
                   3:lambda x:self.A_dict[self.LA[0]].key_range()}
        key_range=key_range[self.kind]
        key_range=key_range(N)
       
       # print(key_range)             
        A=[]
        H=[]
        for key in key_range:
            A.append(self.A_prob[key])
            H.append(self.H_prob[key])
        self.A_features=A
        self.H_features=H
        
    def featurize_team(self, subteam_size=10, N_step=0):
        """ Keyword args subteam_size=10, N_step=0. 
        With default N_step breaks all games into nonintersecting groups 
        of subteam_size, initializes SubTeam instances and computes for each
        probabilities which serve as feature vectors.
        If N_step!=0, takes first subteam_size games as the first group,
        the games from the second to subteam_size+1, and so on to get N_step+1
        groups.
        
        """
        A_Features=[]
        H_Features=[]
        subteams_number=min(len(self.LA),len(self.LH))//subteam_size
        k=0
        if N_step==0:
            for k in range(subteams_number):
                x=self.get_subteam(self.LA[k*subteam_size:(k+1)*subteam_size], 
                                    self.LH[k*subteam_size:(k+1)*subteam_size])
               
                x.feature_prob()
                A_Features.append(x.A_features)
                H_Features.append(x.H_features)
        else:
            for k in range(N_step):
                 x=self.get_subteam(self.LA[k:k+subteam_size], 
                                    self.LH[k:k+subteam_size])               
                 x.feature_prob()
                 A_Features.append(x.A_features)
                 H_Features.append(x.H_features)               
            
        self.label=self.name
        self.A_features=A_Features
        self.H_features=H_Features
        self.feature_map=[{},{}]
        self.feature_map[0][self.label]=self.A_features
        self.feature_map[1][self.label]=self.H_features   
            
    def get_data(self, type_i=1):
        """ Returns tuple (F,l) of feature vectors and labels"""
        temp=[[[key]*len(self.feature_map[type_i][key]), 
               self.feature_map[type_i][key]] for key in self.feature_map[type_i].keys()]
        l_t,f_t=zip(*temp)
        l=[]
        F=[]
        for item in l_t:
            l+=item
        for item in f_t:
            F+=item
        return (F,l)
            
        
    
    def features3D(self,x,y,z,type_i=1,plot=True):
        """ Shows feature vectors in 3d. Args: x,y,z. Keyword args: type_i=1 
        -- Home games statistics (default), type_i=0 -- Away games.
        plot=True -- shows scatter plot if False and plot if True"""
        fig=plt.figure()
        ax=fig.add_subplot('111', projection='3d')
        X=[]
        Y=[]
        Z=[]
        C={}
        X_t={}
        Y_t={}
        Z_t={}
        cols_available=['yellow','brown','violet','magenta','olive','purple','cyan',
                        'blue','green','red','black']
        cols=[]
        
        for item in self.feature_map[type_i].keys():
            if len(cols_available)>0:
                C[item]=cols_available.pop()
            else:
                break
            X_t[item]=[]
            Y_t[item]=[]
            Z_t[item]=[]
            for it in self.feature_map[type_i][item]:
                X.append(it[x])
                Y.append(it[y])
                Z.append(it[z])
                cols.append(C[item])
                X_t[item].append(it[x])
                Y_t[item].append(it[y])
                Z_t[item].append(it[z])
        if not plot:
            ax.scatter(X,Y,Z, c=cols)
        else:
            for item in self.feature_map[type_i].keys():                
                ax.plot3D(X_t[item],Y_t[item],Z_t[item],label=item)
                ax.legend(loc='upper right', shadow=True, fontsize='x-large')
            
            
    def conjugate(self):
        """ Swaps away and home games. -- When one wants to have both 
        on a plot, one can do (Team+Team.conjugate).features3D(...)"""
        temp=[{},{}]         
        for key in self.feature_map[0].keys():                        
            temp[1][key+'t']=self.feature_map[0][key]           
            temp[0][key+'t']=self.feature_map[1][key]            
        self.feature_map=temp
             
        
    def PCA(self,scale_type=None, n_cs=None):
      
        Sc={'Standard':StandardScaler, 'MinMax':MinMaxScaler} 
        #mult_factor={True:len(self.elem_types), False:1}#mult by 2 for C2
        LA=[]
        LH=[]        
        for key in self.feature_map[0].keys():
            LA+=self.feature_map[0][key]                
        for key in self.feature_map[1].keys():
            LH+=self.feature_map[1][key]       
        if scale_type is not None:            
            scalerA=Sc[scale_type]()           
            scalerA.fit(LA)
            LA_scaled=scalerA.transform(LA)
            scalerH=Sc[scale_type]()           
            scalerH.fit(LH)
            LH_scaled=scalerH.transform(LH)
        else:
            LA_scaled=LA
            LH_scaled=LH
        if n_cs is None:
            n_cs=len(LA[0])
        pca=PCA(n_components=n_cs)    
        pca.fit(LA_scaled)        
        pch=PCA(n_components=n_cs)    
        pch.fit(LH_scaled)
        return [pca, pch] 
     
    def get_subteam(self, l_A,l_H):
        return SubTeam(self,l_A,l_H)
    
    def against(self, other):
        l_A=[key for key in self.A_dict.keys() if key in other.H_dict.keys()]
        l_H=[key for key in self.H_dict.keys() if key in other.A_dict.keys()]
        return SubTeam(self, l_A, l_H)
            
    def __iadd__(self, other):
        assert self.kind==other.kind
        self.dict_update(other)
        self.name+=other.name        
        self.feature_map[0].update(other.feature_map[0])
        self.feature_map[1].update(other.feature_map[1])
        self.prob=False        
        return self
    
            
    def __add__(self, other):
        assert self.kind==other.kind
        temp=self.__class__()        
        temp.kind=self.kind
        temp.name=self.name+other.name
        temp.dict_update(self)
        temp.dict_update(other)
        if 'elem_types' in self.__dir__():
            temp.elem_types=self.elem_types        
        temp.feature_map=[{},{}]        
        temp.feature_map[0].update(self.feature_map[0])
        temp.feature_map[1].update(self.feature_map[1])
        temp.feature_map[0].update(other.feature_map[0])
        temp.feature_map[1].update(other.feature_map[1])        
        self.prob=False     
        return temp

class WTeam(Team):   
    
    def __init__(self, team=None, kind=0, prob=False):        
        super().__init__(team=team, kind=kind)
        self.Ln=[0,0]
        self.En=[0,0]       
        self.prob=prob
        if team is not None:
            if self.prob:
                self.get_prob()
        for key in self.A_dict.keys():
            self.elem_types=self.A_dict[key].elem_types
            break
       
    def compute(self,f,N):
        if not self.prob:
            self.get_prob()                  
        F={'log': lambda x:log(x), 'ent': lambda x:x*log(x)}
        Ln={'log':self.Ln, 'ent':self.En}
        Ln=Ln[f]
        f=F[f]
        D_temp={0:self.A_prob, 1:self.H_prob}
        for item in D_temp.keys():
            iters=[key for key in D_temp[item].keys() if key<N]
            Ln[item]=0
            for key in iters:
                Ln[item]-=f(D_temp[item][key])
        return Ln
        
        
    def visualize(self,N=60, fit=30):
        if not self.prob:
            self.get_prob()
        X=[i for i in range(N)]
        temp_dict={0:lambda x:x, 1:lambda x:x, 2:lambda x:(x,)}
        keys=[temp_dict[self.kind](j) for j in X]
        A_prob={key:self.A_prob[key] for key in keys}
        H_prob={key:self.H_prob[key] for key in keys}         
        A_sorted=sorted(A_prob.items(), key=operator.itemgetter(0))
        H_sorted=sorted(H_prob.items(), key=operator.itemgetter(0))
        A_x, A_y=zip(*A_sorted)
        H_x, H_y=zip(*H_sorted)
        
        fig, ax = plt.subplots(figsize=(10,10))

        ax.plot(X, A_y, label='Away')
        ax.plot(X, H_y, label='Home')
        
        if fit and self.kind!=2:
            from scipy import optimize
            def f_func(x,a):
                return (1-a)*a**x
           
            D_y={0:A_y,1:H_y}
            D_title={0:'A_fit',1:'H_fit'}
            for i in range(2):                
                x=X[fit:N]
                y=D_y[i][fit:N]
                pars,pars_cov=optimize.curve_fit(f_func,x,y)
                print(pars)
                print(pars_cov)
                x=X[6:N]
                y=[]
                for item in x:
                    y.append(f_func(item,*pars))
                    
                ax.plot(x,y,label=D_title[i])            
        
        ax.legend(loc='upper right', shadow=True, fontsize='x-large')
        plt.xlabel("Word's length")
        plt.ylabel('Probability')
        ax.set_title(self.name)
        
        #plt.savefig('C:/Users/Owner/Anaconda3/New folder/teams/'+self.name.replace('.','')+'merged'+str(N)+'+'+str(fit))
        
        plt.show()
        
        
    def dist(self, other, N):
        temp_obj=self+other
        temp_comp=temp_obj.compute('ent',N)
        s_comp=self.compute('ent',N)
        o_comp=other.compute('ent',N)
        temp=[]
        for i in range(2):
            temp.append(temp_comp[i]-s_comp[i]-o_comp[i])
        return temp
    
    def most_prob_keys(self):
        self.get_prob()
        A_prb=sorted(self.A_prob.items(), key=operator.itemgetter(1))
        H_prb=sorted(self.H_prob.items(), key=operator.itemgetter(1))
        Ap,_=zip(*A_prb)
        Hp,_=zip(*H_prb)
        return (Ap,Hp)
    
    def featurize(self, word_length=20, elementarity=False, prob_range=False):          
        self.label=self.name        
        init_type={True:lambda:[], False:lambda:Counter()}        
        key_range={0:lambda x:range(x), 1:lambda x:range(x), 2:lambda x:[()]+[(i,) for i in range(x-1)]}
        key_range=key_range[self.kind]
        key_range=key_range(word_length)
        if prob_range:
            key_range=list(self.most_prob_keys()[0][-word_length:])
            key_range.reverse()
        print(key_range)
        Func={True: lambda x:x, False: lambda Cntr: [Cntr[k] for k in key_range]}
         
        A={}
        for key in self.A_dict.keys():
            C1=init_type[elementarity]() 
            C2=init_type[elementarity]()        
            for item in self.elem_types:
                C1+=Func[not elementarity](self.A_dict[key].Dict[0][item]) 
                C2+=Func[not elementarity](self.A_dict[key].Dict[1][item])
            C1=Func[elementarity](C1)
            C2=Func[elementarity](C2)        
            A[key]=C1+C2
        LA=[]         
        gamesA=[key for key in self.A_dict.keys()]    
        for item in gamesA:
            LA.append(A[item])
        self.A_features=LA
        
        H={}        
        for key in self.H_dict.keys():
            C1=init_type[elementarity]() 
            C2=init_type[elementarity]()        
            for item in self.elem_types:
                C1+=Func[not elementarity](self.H_dict[key].Dict[0][item]) 
                C2+=Func[not elementarity](self.H_dict[key].Dict[1][item])
            C1=Func[elementarity](C1)
            C2=Func[elementarity](C2)        
            H[key]=C2+C1
        LH=[]    
        gamesH=[key for key in self.H_dict.keys()]    
        for item in gamesH:
            LH.append(H[item])    
        self.H_features=LH
        self.feature_map=[{self.label:self.A_features}, {self.label:self.H_features}]   
   

        
class RandSubWTeam(WTeam):
    def __init__(self,team, N):
        super().__init__()
        assert N<len(team.A_dict.keys()) and N<len(team.H_dict.keys())        
               
        A_temp=random.sample(team.A_dict.keys(),N)
        H_temp=random.sample(team.H_dict.keys(),N)
        self.elem_types=team.elem_types
        self.A_dict={key:team.A_dict[key] for key in A_temp}
        self.H_dict={key:team.H_dict[key] for key in H_temp}

class SubTeam(WTeam):
    def __init__(self, team, l_A,l_H):
        super().__init__()        
        self.A_dict={key:team.A_dict[key] for key in l_A}
        self.H_dict={key:team.H_dict[key] for key in l_H}
        self.LA=l_A
        self.LH=l_H
        self.kind=team.kind
        self.name='sub'+team.name
        if 'elem_types' in team.__dict__.keys():
            self.elem_types=team.elem_types
        
class STeam(Team):
    def __init__(self,team=None):
        super().__init__(team=team,kind=3)
        self.kind=3
        
    def key_index(self, tup):
        return self.A_dict[self.LA[0]].key_index(tup)
        
    def featurize(self):
        self.label=self.name
        self.A_features=self.A_prob
        self.H_features=self.H_prob
        self.feature_map=[{self.label:self.A_features},{self.label:self.H_features}]
        
    
             
   













        
        