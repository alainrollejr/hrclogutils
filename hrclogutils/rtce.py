# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 15:42:42 2018

@author: aro
"""
import pandas as pd
import numpy as np
import hrclogutils.basic as hrc

# load the rtce log (Real Time Channel Estimator log) into a python pandas dataframe
def load_rtce_log(rtce_path="./sbc_rtce_monitor.csv",rtce_header_path="./sbc_rtce_monitor.headers"):
    df = hrc.load_csv_log(rtce_path,rtce_header_path)
    # enhance with some derived columns
    #df['SCH.Sr'] = df['SCH.Sr'].astype(float)
    #df['SCH.Mc'] = df['SCH.Mc'].astype(float)
    #df['SCH.allocatedRate'] =  0.1*df['SCH.Sr'] * df['SCH.Mc']
    return df;


# filter on terminal id, id should be the 'xyz' string found in 'terminal_xyz'
def filter_name(df, idsubstring): 
    return df[df['name'].str.contains(idsubstring)]

# filter on episodes where terminals are logged on or at least sending power above noise. 
def filter_loggedon(df):
    return df[df['MCD.Signal'].str.contains('Ok')]	

def terminal_averages(df, *arg):  # argument is list of columns to be evaluated (averaged) for the terminal overview
    colString = 'name '; 
    for i in range(len(arg)):
        colString += arg[i]+" "
 
    dfSubset = df.loc[:,colString.split()];
    
    dfSubset.replace('', np.nan, inplace=True) #replace empty entries with Nan
    dfSubset = dfSubset.dropna(axis=0); # drop all rows that contain Nan data, plot tools don't like them
    dfSubset = dfSubset.reindex(); # reindex after plotting
    
    for i in range(len(arg)):
        dfSubset[arg[i]] = dfSubset[arg[i]].astype(float)
    
       
    return pd.pivot_table(dfSubset,index=["name"],values=arg)

def terminal_minmax(df, *arg):  # argument is list of columns to be evaluated (averaged) for the terminal overview
    colString = 'name '; 
    for i in range(len(arg)):
        colString += arg[i]+" "
 
    dfSubset = df.loc[:,colString.split()];
    
    dfSubset.replace('', np.nan, inplace=True) #replace empty entries with Nan
    dfSubset = dfSubset.dropna(axis=0); # drop all rows that contain Nan data, plot tools don't like them
    dfSubset.reindex(); # reindex after plotting
    
    for i in range(len(arg)):
        dfSubset[arg[i]] = dfSubset[arg[i]].astype(float)
        
    return pd.pivot_table(dfSubset,index=["name"],values=arg,aggfunc=[np.min, np.max])