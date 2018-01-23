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
from datetime import datetime, timedelta


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



# filter on a time episode. Start is in past (my birthday) and Stop when I'll be dead, so you can omit either of them
def filter_utc(df,startDateTime="1977-06-02T13:45:30",stopDateTime="2200-06-15T13:45:30"):
    startDateTimeParsed = parse(startDateTime)    
    stopDateTimeParsed = parse(stopDateTime)
    
    if (startDateTimeParsed-stopDateTimeParsed) == timedelta(0):        
        stopDateTimeParsed = startDateTimeParsed + timedelta(seconds=1)
        
    return df[(df['dateTimes'] >= startDateTimeParsed) & (df['dateTimes'] <= stopDateTimeParsed)]

# general purpose tool to reduce the dataframe to list of columns   
def reduce(df, *arg):  # argument is list of columns to be retained
    colString = ''; 
    for i in range(len(arg)):
        colString += arg[i]+" "
 
    dfSubset = df.loc[:,colString.split()];
    
    dfSubset.replace('', np.nan, inplace=True) #replace empty entries with Nan
    dfSubset = dfSubset.dropna(axis=0); # drop all rows that contain Nan data, plot tools don't like them
    dfSubset.reindex(); # reindex after plotting    
    return dfSubset;



# general purpose tool to plot column(s) from the log vs UTC time and SOF time (two x axis)
def plot_utc_sof(df, *arg): # argument is list of headers to be plotted
    colString = 'dateTimes sof ';  
    for i in range(len(arg)):
        print(arg[i]) 
        colString += arg[i]+" "
  
    dfSubset = df.loc[:,colString.split()];
    dfSubset.replace('', np.nan, inplace=True) #replace empty entries with Nan
    dfSubset = dfSubset.dropna(axis=0); # drop all rows that contain Nan data, plot tools don't like them
    dfSubset.reindex(); # reindex after dropping   
    
    
    fig, ax = plt.subplots()
    for parameterHeaderName in arg:
        v = dfSubset[parameterHeaderName].values
        plt.plot(dfSubset['dateTimes'],v.astype(np.float),label=parameterHeaderName, marker='o') 
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S\n\n%Y%m%d'))
    plt.xlabel('time (UTC)')  
    
    
    ax2 = ax.twiny()
    for parameterHeaderName in arg:
        v = dfSubset[parameterHeaderName].values
        plt.plot(dfSubset['sof'],v.astype(np.float),label=parameterHeaderName, marker='o') 
    ax2.ticklabel_format(useOffset=False)
    plt.xlabel('sof time (seconds since boot of PTP master)')
    
    
    plt.legend(loc='best') 
    ax.yaxis.grid() # horizontal lines
    ax.xaxis.grid() # vertical lines   
    plt.show()  
    
# general purpose tool to plot a column(s) that contains strings  vs UTC time and SOF time (two x axis)
def plot_str_utc_sof(df, *arg): # argument is list of headers to be plotted    
    colString = 'dateTimes sof '+arg[0];  
    
    dfSubset = df.loc[:,colString.split()];
    dfSubset.replace('', np.nan, inplace=True) #replace empty entries with Nan
    dfSubset = dfSubset.dropna(axis=0); # drop all rows that contain Nan data, plot tools don't like them
    dfSubset.reindex(); # reindex after dropping   
    
    keys = dfSubset[arg[0]].unique() # labels in second argument
    ind = np.arange(len(keys)) # the y locations for the groups
    width = 10.0       # the width of the tick separation
    
    dictionary = dict(zip(keys, ind))
    dfSubset.replace({arg[0]: dictionary}) # replace the strings by their ind values used for plotting
  
    fig, ax1 = plt.subplots()
   
    ax1.set_yticks(ind + width / 2)
    ax1.set_yticklabels(keys)  
    
    
       
    plt.plot(dfSubset['dateTimes'],dfSubset[arg[0]],label=arg[0], marker='o') 
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S\n\n%Y%m%d'))
    plt.xlabel('time (UTC)')  
    
    
    ax2 = ax1.twiny()
    plt.plot(dfSubset['sof'],dfSubset[arg[0]],label=arg[0], marker='o')     
    #ax2.ticklabel_format(useOffset=False)
    plt.xlabel('sof time (seconds since boot of PTP master)')
    
    
    plt.legend(loc='best') 
    ax2.yaxis.grid() # horizontal lines
    ax2.xaxis.grid() # vertical lines   
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
    
# general purpose tool to plot 2 columns from the log vs each other 
def plot_xcor(df, *arg):  # argument is list of the 2 headers to be plotted vs each other
    colString = ''; 
    for i in range(len(arg)):
        colString += arg[i]+" "
 
    dfSubset = df.loc[:,colString.split()];
    dfSubset.replace('', np.nan, inplace=True) #replace empty entries with Nan
    dfSubset = dfSubset.dropna(axis=0); # drop all rows that contain Nan data, plot tools don't like them
    dfSubset.reindex(); # reindex after plotting  
    

    x = dfSubset[arg[0]].values      
    y = dfSubset[arg[1]].values
    
    fig, ax = plt.subplots()
    
    plt.scatter(x.astype(float),y.astype(np.float)) 
    
    plt.xlabel(arg[0])
    plt.ylabel(arg[1])
    plt.legend(loc='best')  
    ax.yaxis.grid() # horizontal lines
    ax.xaxis.grid() # vertical lines 
    plt.show()
    
# general purpose tool to plot 1 columns from dataframe as pie chart
def plot_pie(df, *arg):  # argument is column and label
    x = df[arg[0]].values  
    #print("pie of " + str(x)) 
    lab = df[arg[1]]
 
    fig, ax = plt.subplots()
    plt.pie(x.astype(float),labels=lab) 
    plt.legend(loc='best')  
    plt.title('Pie chart distribution of ' + arg[0])
    plt.show()    
    
def plot_bar(df, *arg):
    x = df[arg[0]].values  # values in first argument
    
    lab = df[arg[1]] # labels in second argument
    ind = np.arange(len(lab)) # the x locations for the groups
    width = 0.35       # the width of the bars
  
    fig, ax = plt.subplots()
    ax.bar(ind,x)
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(lab)
    plt.title('Bar chart  of ' + arg[0])
    plt.show()

	