# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 15:42:42 2018

@author: aro
"""
import pandas as pd
import numpy as np
import hrclogutils.basic as hrc
import matplotlib.pyplot as plt

# load the rtce log (Real Time Channel Estimator log) into a python pandas dataframe
def load_rtce_log(rtce_path="./sbc_rtce_monitor.csv",rtce_header_path="./sbc_rtce_monitor.headers"):
    df = hrc.load_csv_log(rtce_path,rtce_header_path)
    # enhance with some derived columns
    tmp, df['id'] = df['name'].str.split('_', 1).str    
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

# filter on episodes where terminals are logged on or at least sending power above noise. 
def filter_loggingon(df):
    return df[df['SCH.Mc'].str.contains('InvalidModcod')]	

def filter_assigned_to_demod(df):
    return df[df['demod']!=""]

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

def plot_spectrum(df,spectrumDateTime):
    dfSlice = df.pipe(hrc.filter_utc,startDateTime=spectrumDateTime,stopDateTime=spectrumDateTime).pipe(filter_assigned_to_demod)
    print(dfSlice['demod'])
    
    # sort by carrier freq
    dfSlice = dfSlice.sort_values(['SCH.f'], ascending=True)
    minval = -175.0
    freq_corners = np.zeros(shape=(4*len(dfSlice.index),1) )
    psd_corners = np.zeros(shape=(4*len(dfSlice.index),1) )
    i = 0
    fig, ax = plt.subplots()
    
    for index, row in dfSlice.iterrows():        
        print(row['SCH.f'])
        center_freq = float(row['SCH.f'])
        cr = float(row['SCH.Cr'])
        sig_psd = float(row['MCD.Co'])
        #noise_psd = sig_psd - float(row['MCD.EsNo'])
        start_freq = center_freq - 0.5*cr
        stop_freq = center_freq + 0.5*cr
        freq_corners[i] = start_freq - 1
        psd_corners[i] = minval
        i = i+1
        freq_corners[i] = start_freq
        psd_corners[i] =  sig_psd
        i = i+1
        freq_corners[i] = stop_freq
        psd_corners[i] =  sig_psd
        i = i+1
        freq_corners[i] = stop_freq +1
        psd_corners[i] =  minval
        i = i+1
        
        ax.annotate(row['name'], xy=(center_freq,minval+10), rotation = 90)
        
    
    
    plt.plot(freq_corners,psd_corners,'.-') 
    
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('psd')
    
    ax.yaxis.grid() # horizontal lines
    ax.xaxis.grid() # vertical lines 
    plt.show()
    