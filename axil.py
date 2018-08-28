# -*- coding: utf-8 -*-
"""
This module contains the definition of function probs(N) which
computes probabilities of sequences of zeroes (absence of a shot) and
ones (a shot) of length N (time interval of N seconds), and saves the
corresponding dictionaries in text files as json objects.
"""


import json
import os


def probs(N=10):
    
    fdir='C:\\Users\\Owner\\Anaconda3\\New folder'

    f=open(fdir+'\\Games.txt', 'rt')
    jf=json.load(f)
    f.close()

    Prob=[{}, {}]
    count=0
    total_interval=[0,0]
    for game in jf.keys():
        i_team=0
        for team in jf[game]:
            times=[item[0] for item in team]
            t_min=times[0]
            t_max=times[-1]
            t_range=range(min(0, t_min-N+1), t_max+1)
            t_interval=set(t_range)
            total_interval[i_team]+=len(t_interval)
            for time in times:
                time_set=set(range(time-N+1, time+1))
                time_interval=t_interval.intersection(time_set)
                for moment in time_interval:
                    i=0
                    s=''
                    while i<N:
                        if (moment+i) in times:
                            s+='1'
                        else:
                            s+='0'
                        i+=1
                    if s in Prob[i_team].keys():
                        Prob[i_team][s]+=1
                    else:
                        Prob[i_team][s]=1
                t_interval-=set(time_interval)
            all_zeros=N*'0'
            if all_zeros in Prob[i_team].keys():
                Prob[i_team][all_zeros]+=len(t_interval)
            else:
                Prob[i_team][all_zeros]=len(t_interval)
            
            i_team=1
        count+=1
        #print(count)
    if 'Correlators' not in os.listdir(fdir):
        os.mkdir(fdir+'\\Correlators')
    os.chdir(fdir+'\\Correlators')
    f=open('numbers'+str(N)+'.txt', 'wt')
    json.dump(Prob, f)
    f.close()
    for team in range(2):
        for item in Prob[team].keys():
            Prob[team][item]=Prob[team][item]/total_interval[team]
    f=open('probs'+str(N)+'.txt', 'wt')
    json.dump(Prob, f)
    f.close()
    os.chdir(fdir)
    return Prob
            
        
            
            
    