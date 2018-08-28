# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 22:52:51 2018

@author: Owner
"""

def group_stat(W_dict):
    temp=''
    for key in W_dict.keys():
        temp=key
        break    
    a=W_dict[temp].__class__()
    for key in W_dict.keys():
        a+=W_dict[key]
    
    if 'activation' in a.__dir__():
        raise GetProbException(a)        
    temp=a.get_prob()                 
    return temp

class GetProbException(Exception):
    def __init__(self,a):
        super().__init__()
        self.temp=a.get_prob()
        self.Attack=a.Attack
        self.activation=a.activation
        
        
        