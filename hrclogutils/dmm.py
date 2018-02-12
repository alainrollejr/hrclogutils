# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 07:30:27 2018

@author: aro
"""

from mpl_toolkits.basemap import Basemap

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import matplotlib.dates as mdates
import re



"""
    if a dataframe contains lat and long columns, plot them on a basemap
"""
def scatter_on_basemap(df, title='scatter on basemap'):
    # create new figure, axes instances.
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])
    # setup mercator map projection.
    
    llcrnrlon=min(df['long'])-5.
    llcrnrlat=min(df['lat'])-5.
    urcrnrlon=max(df['long'])+20. # leave room for legend
    urcrnrlat=max(df['lat'])+5.
    
    m = Basemap(llcrnrlon,llcrnrlat,urcrnrlon,urcrnrlat,\
                rsphere=(6378137.00,6356752.3142),\
                resolution='l',projection='merc',\
                lat_0=40.,lon_0=-20.,lat_ts=20.)
 
    
    m.drawlsmask(land_color='palegreen', ocean_color='aqua') 
    m.fillcontinents(color='palegreen',lake_color='blue',zorder=0)
    m.drawcountries()
    m.drawstates()
    m.drawcoastlines()
    
    
    # draw parallels
    m.drawparallels(np.arange(-70,80,5),labels=[1,1,0,1])
    
    # draw meridians
    m.drawmeridians(np.arange(-180,180,5),labels=[1,1,0,1])
    
    macList = df['mac'].unique()
    colorList = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    markerList = ['o', 'v','<','D','s','*']
    
    colorInd = 0
    markerInd = 0
    count = 0
    for mac in macList:
        dfSubset = df[df['mac']==mac]
        labelString = str(mac)
        lons, lats = m(dfSubset['long'].values.astype(float), dfSubset['lat'].values.astype(float))
        print(str(mac) + ':' + str(len(lons)) + ' coordinates shown on map' )
        m.plot(lons,lats,marker=markerList[markerInd],color=colorList[colorInd], label=labelString)
        
        colorInd = (colorInd +1) % len(colorList)
        markerInd = (markerInd +1) % len(markerList)
        count = count + 1
        
    title_str = title + ' (' + str(count) + ' terminals shown)\n' + 'data taken from ' + str(min(df['dateTimes'])) + ' to ' + str(max(df['dateTimes']))
    ax.set_title(title_str)
    print(title_str)
    if count < 35: # too much is too much, for a legend
        plt.legend(loc='upper right')
    plt.show()
    
def beams_on_basemap(df, title='scatter on basemap'):
    # create new figure, axes instances.
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])
    # setup mercator map projection.
    
    llcrnrlon=min(df['long'])-5.
    llcrnrlat=min(df['lat'])-5.
    urcrnrlon=max(df['long'])+20. # leave room for legend
    urcrnrlat=max(df['lat'])+5.
    
    m = Basemap(llcrnrlon,llcrnrlat,urcrnrlon,urcrnrlat,\
                rsphere=(6378137.00,6356752.3142),\
                resolution='l',projection='merc',\
                lat_0=40.,lon_0=-20.,lat_ts=20.)
 
    
    m.drawlsmask(land_color='palegreen', ocean_color='aqua') 
    m.fillcontinents(color='palegreen',lake_color='blue',zorder=0)
    m.drawcountries()
    m.drawstates()
    m.drawcoastlines()
    
    
    # draw parallels
    m.drawparallels(np.arange(-70,80,5),labels=[1,1,0,1])
    
    # draw meridians
    m.drawmeridians(np.arange(-180,180,5),labels=[1,1,0,1])
    
    beamList = df['activebeam'].unique()
    colorList = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    markerList = ['o', 'v','<','D','s','*']
    
    colorInd = 0
    markerInd = 0
    count = 0
    for beam in beamList:
        dfSubset = df[df['activebeam']==beam]
        labelString = str(beam)
        lons, lats = m(dfSubset['long'].values.astype(float), dfSubset['lat'].values.astype(float))
        m.scatter(lons,lats,marker=markerList[markerInd],color=colorList[colorInd], label=labelString)
        
        colorInd = (colorInd +1) % len(colorList)
        markerInd = (markerInd +1) % len(markerList)
        count = count + 1
        
    
    ax.set_title(title + ' (' + str(count) + ' active beams shown)\n' + 'data taken from ' + str(min(df['dateTimes'])) + ' to ' + str(max(df['dateTimes'])))
    plt.legend(loc='upper right')
    plt.show()
    
    
    
# general purpose tool to plot a column(s) that contains strings  vs UTC time and SOF time (two x axis)
def plot_str_utc(df, *arg): # argument is list of headers to be plotted    
    colString = 'dateTimes '+arg[0];  
    
    dfSubset = df.loc[:,colString.split()];
    dfSubset.replace('', np.nan, inplace=True) #replace empty entries with Nan
    dfSubset = dfSubset.dropna(axis=0); # drop all rows that contain Nan data, plot tools don't like them
    dfSubset.reindex(); # reindex after dropping   
    
    keys = dfSubset[arg[0]].unique() # labels in second argument
    
    ind = np.arange(len(keys)) # the y locations for the groups
    #print(ind)
    width = 10.0       # the width of the tick separation
    
    dictionary = dict(zip(keys, ind))
    #print(dictionary)
    dfSubset.replace({arg[0]: dictionary}, inplace=True) # replace the strings by their ind values used for plotting
  
    #print(dfSubset.head())
    
    fig, ax1 = plt.subplots()
   
    
    
       
    line = ax1.plot(dfSubset['dateTimes'],dfSubset[arg[0]],label=arg[0], marker='o') 
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S\n\n%Y%m%d'))
    plt.xlabel('time (UTC)')   

    #ax1.set_yticks(ind + width / 2)
    #ax1.set_yticklabels(keys) 
    ax1.set_yticks(ind)
    ax1.set_yticklabels(keys)        
    
    plt.legend(loc='best') 
    
    ax1.grid(b=True, which='major', color='b', linestyle='-')
    
    
    plt.show() 
    
"""
    make a dmm dataframe based on 
        "Response: \"GetMobileInfo\""
    entries in dmm.log
    
    Note: 
        GetMobileinfo gets called by PAC statera quite irregularly per MAC.
        it may come every 15sec or every hour
        Other calls like GetMobileInfoList or GetMobileInfoStats come regularly
        but the dmm log abbreviates the large response to them, making it difficult to
        use the log lines for getting useful info for all terminals.
        other candidates 
"""
def mobile_info_to_dataframe(path, macstring=None):
    with open(path,"r") as f:
        #file_content = f.read().rstrip("\n") # if you don't want end of lines
        file_content = f.read()       
    
    
    """
        first find all mac addresses
    """
    p = re.compile(r'([0-9a-f]{2}(?::[0-9a-f]{2}){5})', re.IGNORECASE)   

    mac_list = re.findall(p, file_content)   
    
    if macstring is None:
        mac_list_unique = set(mac_list) #convert list to a set
    else:
        mac_list_unique = [macstring]
    #print(mac_list_unique)
    #print(str(len(mac_list_unique)) + ' unique mac addresses found')    

    columns = ['dateTimes','mac', 'located','activebeam','lat', 'long']
    df = pd.DataFrame(columns=columns)
    df = df.fillna(0) # with 0s rather than NaNs
    
    for line in file_content.splitlines():
        if "Response: \"GetMobileInfo\"" in line:
            date = datetime.datetime.strptime(line[0:20],"%y/%m/%d-%H:%M:%S.%f")
            #date = parse(line[0:20]) 
            
            temp_list = re.split("[{}=;\']+",line)
            #print(temp_list)
            
            mobile_info_date = date
            mobile_info_mac = "00:00:00:00:00:00"
            mobile_info_located = False
            mobile_info_beam = "dummybeam"
            mobile_info_longitude = 0.0
            mobile_info_latitude = 0.0
            
            terminal_match = False
            
            for ind, element in enumerate(temp_list):
                element = element.strip() # remove accidental white space from string
                #print(str(ind) + "=" + element)
                if element in mac_list_unique:
                    # add a row to the dataframe
                    mobile_info_mac = element
                    mobile_info_date = date
                    mobile_info_located = False
                    terminal_match = True
                    
                    
                if "operational/located" in element:
                    mobile_info_located = True
                    
                    
                if "active-beam" in element:
                    mobile_info_beam = temp_list[ind+1]
                    
                if "longitude" in element:
                    mobile_info_longitude = float(temp_list[ind+1])
                    
                if "latitude" in element:
                    mobile_info_latitude = float(temp_list[ind+1])                    
                    # this was the last thing about this mac address we wanted to put in table row
                    row=pd.Series([mobile_info_date, mobile_info_mac,
                                   mobile_info_located,mobile_info_beam,
                                   mobile_info_latitude, mobile_info_longitude],columns)
    
                    if terminal_match == True:
                        df = df.append([row],ignore_index=True)
                        terminal_match = False
                        
    df['dateTimes'] = df['dateTimes'].dt.round('S')
                    
    return df

"""
    make a dmm dataframe based on 
        Response: "GetStatistics"
    entries in dmm.log
"""
def stats_to_dataframe(path):
    with open(path,"r") as f:
        #file_content = f.read().rstrip("\n") # if you don't want end of lines
        file_content = f.read()       
    
     

    columns = ['dateTimes','located','operational','switch_request','switch_success']
    df = pd.DataFrame(columns=columns)
    df = df.fillna(0) # with 0s rather than NaNs
    
    for line in file_content.splitlines():
        if "Response: \"GetStatistics\"" in line:
            date = datetime.datetime.strptime(line[0:20],"%y/%m/%d-%H:%M:%S.%f")
            #date = parse(line[0:20]) 
            
            temp_list = re.split("[{}=;\']+",line)
            #print(temp_list)
            
            mobile_info_date = date            
            mobile_info_located = -1
            mobile_info_operational = -1
            mobile_info_switch_request = -1
            mobile_info_switch_success = -1
            
            
            
            for ind, element in enumerate(temp_list):
                element = element.strip() # remove accidental white space from string
                
                if "switch-request"==element:
                    mobile_info_switch_request = int(temp_list[ind+1])
                    
                if "switch-success"==element:
                    mobile_info_switch_success = int(temp_list[ind+1])
                    
                if "located"==element:
                    mobile_info_located = int(temp_list[ind+1])
                    
                    
                if "operational"==element:
                    mobile_info_operational = int(temp_list[ind+1])
                    
                
                    row=pd.Series([mobile_info_date, mobile_info_located,
                                   mobile_info_operational,mobile_info_switch_request,mobile_info_switch_success],columns)
    
                    
                    df = df.append([row],ignore_index=True)
                        
    df['dateTimes'] = df['dateTimes'].dt.round('S')
                    
    return df

"""
    make a  dataframe based on anomalies in the log file
"""
def anomalies_to_dataframe(path):
    with open(path,"r") as f:
        #file_content = f.read().rstrip("\n") # if you don't want end of lines
        file_content = f.read()       

    columns = ['dateTimes','error']
    df = pd.DataFrame(columns=columns)
    df = df.fillna(0) # with 0s rather than NaNs
    
    for line in file_content.splitlines():
        if "disconnected" in line:
            date = datetime.datetime.strptime(line[0:20],"%y/%m/%d-%H:%M:%S.%f")   
            error_str = line[21:-1]   
            row=pd.Series([date, error_str],columns)                    
            df = df.append([row],ignore_index=True)
            print(line)
            
        if "Failure" in line:
            date = datetime.datetime.strptime(line[0:20],"%y/%m/%d-%H:%M:%S.%f")   
            error_str = line[21:-1]   
            row=pd.Series([date, error_str],columns)                    
            df = df.append([row],ignore_index=True)
            print(line)
            
    if len(df) > 0:                    
        df['dateTimes'] = df['dateTimes'].dt.round('S')
                    
    return df

def changes_to_dataframe(path, macstring=None):
    with open(path,"r") as f:
        #file_content = f.read().rstrip("\n") # if you don't want end of lines
        file_content = f.read()     
        
    """
        first find all mac addresses
    """
    p = re.compile(r'([0-9a-f]{2}(?::[0-9a-f]{2}){5})', re.IGNORECASE)   

    mac_list = re.findall(p, file_content)   
    
    if macstring is None:
        mac_list_unique = set(mac_list) #convert list to a set
    else:
        mac_list_unique = [macstring]
        
    #print(mac_list_unique)

    columns = ['dateTimes','mac','operational','located']
    df = pd.DataFrame(columns=columns)
    df = df.fillna(0) # with 0s rather than NaNs
    
    for line in file_content.splitlines():
        if "changes" in line:
            if "terminalNoTxZone" not in line:
                for mac in mac_list_unique:
                    if mac in line:
                        date = datetime.datetime.strptime(line[0:20],"%y/%m/%d-%H:%M:%S.%f")                          
          
                        mobile_info_mac = mac
                        mobile_info_date = date
                                               
                         
                        if "nonoperational" in line:
                            mobile_info_operational = 0
                        else:
                            mobile_info_operational = 1
                            
                        if "unlocated" in line:
                            mobile_info_located = 0
                        else:
                            mobile_info_located = 1
                             
                         
                        row=pd.Series([mobile_info_date, mobile_info_mac,
                                       mobile_info_operational, mobile_info_located],columns)
                        df = df.append([row],ignore_index=True)                 
           
      
        
            
    if len(df) > 0:                    
        df['dateTimes'] = df['dateTimes'].dt.round('S')
    else:
        print('no changes found')
                    
    return df