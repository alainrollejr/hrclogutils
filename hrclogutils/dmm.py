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
    urcrnrlon=max(df['long'])+5.
    urcrnrlat=max(df['lat'])+5.
    
    m = Basemap(llcrnrlon,llcrnrlat,urcrnrlon,urcrnrlat,\
                rsphere=(6378137.00,6356752.3142),\
                resolution='l',projection='merc',\
                lat_0=40.,lon_0=-20.,lat_ts=20.)
    """
    m = Basemap(llcrnrlon=-180.,llcrnrlat=-70.,urcrnrlon=180.,urcrnrlat=80.,projection='merc')
   """
    m.drawcoastlines(zorder=0)
    m.fillcontinents(zorder=0)
    m.drawcountries()
    m.drawstates()
    
    # draw parallels
    m.drawparallels(np.arange(-70,80,5),labels=[1,1,0,1])
    
    # draw meridians
    m.drawmeridians(np.arange(-180,180,5),labels=[1,1,0,1])
    
    lons, lats = m(df['long'].values.astype(float), df['lat'].values.astype(float))
    m.scatter(lons,lats,marker='D',color='m')
    
    ax.set_title(title)
    plt.show()
    
"""
    make a dmm dataframe based on 
        "Response: \"GetMobileInfo\""
    entries in dmm.log
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
    print(str(len(mac_list_unique)) + ' unique mac addresses found')    

    columns = ['dateTime','mac', 'located','activebeam','lat', 'long']
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
            
            for ind, element in enumerate(temp_list):
                element = element.strip() # remove accidental white space from string
                #print(str(ind) + "=" + element)
                if element in mac_list_unique:
                    # add a row to the dataframe
                    mobile_info_mac = element
                    mobile_info_date = date
                    mobile_info_located = False
                    
                    
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
                    df = df.append([row],ignore_index=True)
                    
    return df