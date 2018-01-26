# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 07:30:27 2018

@author: aro
"""

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

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
   
    m.drawcoastlines()
    m.fillcontinents()
    # draw parallels
    m.drawparallels(np.arange(10,90,20),labels=[1,1,0,1])
    # draw meridians
    m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])
    m.scatter(df['lat'],df['long'],3,marker='o',color='k')
    
    ax.set_title(title)
    plt.show()