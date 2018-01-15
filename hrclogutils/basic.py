# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 23:44:54 2018

@author: aro

    Python Module containing utilities to execute common manipulations and
    investigations on HRC log files generated by the HRC controller.
    
    Warning: most utilities require the a dialog version of at least 1.3.1.6,
    because UTC time was absent from logs before that dialog release

    Most utilities are functions that can be "piped". Order of execution is 
    from left pipe to rightmost pipe, see the example files
"""


import pandas as pd
import numpy as np
from dateutil.parser import parse


import matplotlib.dates as mdates
import matplotlib.pyplot as plt

# load .csv file into a python pandas dataframe
def load_csv_log(path,header_path):
    hdf = pd.read_csv(header_path)
    df = pd.read_csv(path, header=None, keep_default_na=False) # leaves whitespaces in
    #df = pd.read_csv(rtce_path, header=None) # whitespaces become nan
    df.columns=hdf.columns.values.tolist()

    # convert time to datetime object'    
    df['dateTimes'] = pd.to_datetime(df['utc'], format='%Y%m%dT%H%M%S.%f')
    return df

# load the rtce log (Real Time Channel Estimator log) into a python pandas dataframe
def load_rtce_log(rtce_path="./sbc_rtce_monitor.csv",rtce_header_path="./sbc_rtce_monitor.headers"):
    df = load_csv_log(rtce_path,rtce_header_path)
    # enhance with some derived columns
    #df['SCH.allocatedRate'] =  df['SCH.Sr'].values.astype(np.float) * df['SCH.Mc'].values.astype(np.float)
    return df;

# filter on terminal id, id should be the 'xyz' string found in 'terminal_xyz'
def filter_name(df, idsubstring): 
    return df[df['name'].str.contains(idsubstring)]

# filter on a time episode. Start is in past (my birthday) and Stop when I'll be dead, so you can omit either of them
def filter_utc(df,startDateTime="1977-06-02T13:45:30",stopDateTime="3000-06-15T13:45:30"):
    startDateTimeParsed = parse(startDateTime)
    stopDateTimeParsed = parse(stopDateTime)
    return df[(df['dateTimes'] >= startDateTimeParsed) & (df['dateTimes'] <= stopDateTimeParsed)]

# filter on episodes where terminals are logged on or at least sending power above noise. 
def filter_loggedon(df):
    return df[df['MCD.Signal'].str.contains('Ok')]	

# general purpose tool to plot column(s) from the log vs UTC time and SOF time (two x axis)
def plot_utc_sof(df, *arg): # argument is list of headers to be plotted
    colString = 'dateTimes sof ';  
    for i in range(len(arg)):
        print(arg[i]) 
        colString += arg[i]+" "
  
    dfSubset = df.loc[:,colString.split()];
    dfSubset.replace('', np.nan, inplace=True) #replace empty entries with Nan
    dfSubset = dfSubset.dropna(axis=0); # drop all rows that contain Nan data, plot tools don't like them
    dfSubset.reindex(); # reindex after plotting   
    
    
    fig, ax = plt.subplots()
    for parameterHeaderName in arg:
        v = dfSubset[parameterHeaderName].values
        plt.plot(dfSubset['dateTimes'],v.astype(np.float),label=parameterHeaderName) 
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S\n\n%Y%m%d'))
    plt.xlabel('time (UTC)')  
    
    
    ax2 = ax.twiny()
    for parameterHeaderName in arg:
        v = dfSubset[parameterHeaderName].values
        plt.plot(dfSubset['sof'],v.astype(np.float),label=parameterHeaderName) 
    ax2.ticklabel_format(useOffset=False)
    plt.xlabel('sof time (seconds since boot of PTP master)')
    
    
    plt.legend(loc='best') 
    ax.yaxis.grid() # horizontal lines
    ax.xaxis.grid() # vertical lines   
    plt.show()    
    
# general purpose tool to plot column(s) from the log vs UTC time
def plot_utc(df, *arg): # argument is list of headers to be plotted
    colString = 'dateTimes ';  
    for i in range(len(arg)):
        print(arg[i]) 
        colString += arg[i]+" "
  
    dfSubset = df.loc[:,colString.split()];
    dfSubset.replace('', np.nan, inplace=True) #replace empty entries with Nan
    dfSubset = dfSubset.dropna(axis=0); # drop all rows that contain Nan data, plot tools don't like them
    dfSubset.reindex(); # reindex after plotting   
    
    
    fig, ax = plt.subplots()
    for parameterHeaderName in arg:
        v = dfSubset[parameterHeaderName].values
        plt.plot(dfSubset['dateTimes'],v.astype(np.float),label=parameterHeaderName) 
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S\n\n%Y%m%d'))
    plt.xlabel('time (UTC)')   
    plt.legend(loc='best') 
    ax.yaxis.grid() # horizontal lines
    ax.xaxis.grid() # vertical lines     
    plt.show() 

# general purpose tool to plot column(s) from the log vs SOF time   
def plot_sof(df, *arg):  # argument is list of headers to be plotted
    colString = 'sof '; 
    for i in range(len(arg)):
        print(arg[i]) 
        colString += arg[i]+" "
 
    dfSubset = df.loc[:,colString.split()];
    dfSubset.replace('', np.nan, inplace=True) #replace empty entries with Nan
    dfSubset = dfSubset.dropna(axis=0); # drop all rows that contain Nan data, plot tools don't like them
    dfSubset.reindex(); # reindex after plotting
    
    

    sofs = dfSubset['sof'].values      
    fig, ax = plt.subplots()
    for parameterHeaderName in arg:
        v = dfSubset[parameterHeaderName].values
        plt.plot(sofs,v.astype(np.float),label=parameterHeaderName) 
    # Set y limits
    ax.ticklabel_format(useOffset=False)
    plt.xlabel('sof time (seconds since boot of PTP master)')
    plt.legend(loc='best')  
    ax.yaxis.grid() # horizontal lines
    ax.xaxis.grid() # vertical lines 
    plt.show()    

	