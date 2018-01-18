# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 15:42:42 2018

@author: aro
"""
import pandas as pd
import numpy as np
import hrclogutils.basic as hrc


# load the rtce log (Real Time Channel Estimator log) into a python pandas dataframe
def load_carrier_log(path="./sbc_carrier_tracking_monitor.csv",
                     header_path="./sbc_carrier_tracking_monitor.headers"):
    df = hrc.load_csv_log(path,header_path)
     # enhance with some derived columns        
    df['modcod'] = df['modcod'].astype(float)
    df['curSymbRate(Bd)'] = df['curSymbRate(Bd)'].astype(float)
    df['spreadingFactor'] = df['spreadingFactor'].astype(float)
    df['efficiency(bits/symbol)'] = 0.1 * df['modcod']  / df['spreadingFactor']
    df['allocatedRate(bits/s)'] =  df['efficiency(bits/symbol)']*df['curSymbRate(Bd)']    
    return df;

# filter on terminal id, id should be the 'xyz' string found in 'terminal_xyz'
def filter_terminal(df, idsubstring): 
    return df[df['terminal'].str.contains(idsubstring)]


def packet_error_analysis(idsubstring,    # only mandatory parameter               
                   path="./sbc_carrier_tracking_monitor.csv",
                   header_path="./sbc_carrier_tracking_monitor.headers", 
                   startDateTime="1977-06-02T13:45:30",
                   stopDateTime="2200-06-15T13:45:30"):
    
    df = load_carrier_log(path, header_path)
    
    dfSubset = df.pipe(filter_terminal, idsubstring).pipe(hrc.filter_utc,startDateTime,stopDateTime)
    
    
    dfSubset.replace('', np.nan, inplace=True) #replace empty entries with Nan
    dfSubset = dfSubset.dropna(axis=0); # drop all rows that contain Nan data, plot tools don't like them
    dfSubset.reindex(); # reindex after dropping
    
    vDec = dfSubset['prevDecPackCnt'].values
    vTot = dfSubset['prevTotPackCnt'].values
    
    vPerProcent = 100.0 * (vTot.astype(np.float) - vDec.astype(np.float))/vTot.astype(np.float)
    
    # errored packets from frame N are reported in frame N+2
    dfSubset['perProcent'] = np.roll(vPerProcent,-2)       
   
    
    dfSubset.pipe(hrc.plot_utc_sof,'perProcent')
    
    # create a list with columns worth retaining for a crosscorrelation
    dfCrossList = ['curEsNo(dB)','curFreqErrorPreamble','curSymbolRateTimingErrorPreamble','agcFailure',
                   'modcod','chipRateMultiplicator','spreadingFactor',
                   'agcFailure']    
        
    for h in dfCrossList:       
        dfSubset.pipe(hrc.plot_xcor,h,'perProcent')  
        
def terminal_averages(df, *arg):  # argument is list of columns to be evaluated (averaged) for the terminal overview
    colString = 'terminal '; 
    for i in range(len(arg)):
        colString += arg[i]+" "
 
    dfSubset = df.loc[:,colString.split()];
    
    dfSubset.replace('', np.nan, inplace=True) #replace empty entries with Nan
    dfSubset = dfSubset.dropna(axis=0); # drop all rows that contain Nan data, plot tools don't like them
    dfSubset.reindex(); # reindex after plotting
    
    for i in range(len(arg)):
        dfSubset[arg[i]] = dfSubset[arg[i]].astype(float)
    
    return pd.pivot_table(dfSubset,index=["terminal"],values=arg)

def terminal_minmax(df, *arg):  # argument is list of columns to be evaluated (averaged) for the terminal overview
    colString = 'terminal '; 
    for i in range(len(arg)):
        colString += arg[i]+" "
 
    dfSubset = df.loc[:,colString.split()];
    
    dfSubset.replace('', np.nan, inplace=True) #replace empty entries with Nan
    dfSubset = dfSubset.dropna(axis=0); # drop all rows that contain Nan data, plot tools don't like them
    dfSubset.reindex(); # reindex after plotting
    
    for i in range(len(arg)):
        dfSubset[arg[i]] = dfSubset[arg[i]].astype(float)
    
    return pd.pivot_table(dfSubset,index=["terminal"],values=arg,aggfunc=[np.min, np.max])
    
    
    
    