# -*- coding: utf-8 -*-
"""
This module contains the definition of function 'cond_probs' which
computes conditional probabilities of events in games based
on probabilities computed by the script 'axil.py' and saved as json files.
"""
import json



def cond_probs(N):
    Cond_Probs=[{},{}]
    fdir='C:\\Users\\Owner\\Anaconda3\\New folder\\Correlators\\'
    fN=open(fdir+'probs'+str(N)+'.txt', 'rt')
    fN_1=open(fdir+'probs'+str(N-1)+'.txt', 'rt')
    jN=json.load(fN)
    jN_1=json.load(fN_1)
    fN.close()
    fN_1.close()    
    for team in range(2):
        for key in jN[team].keys():
            if key[:-1] in jN_1[team].keys():
                Cond_Probs[team][key[-1]+'|'+key[:-1]]=jN[team][key]/jN_1[team][key[:-1]]
    f=open(fdir+'Cond'+str(N)+'.txt', 'wt')
    json.dump(Cond_Probs, f)
    f.close()
    return Cond_Probs