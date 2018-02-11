# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 23:53:29 2018

 script to check mobility flows related to a terminal
 
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import hrclogutils.dmm as dmm
import hrclogutils.basic as hrc
import pandas as pd
import matplotlib.pyplot as plt


def main(argv):
    
    parser = argparse.ArgumentParser(description='script to check mobility flows related to a terminal')
    
    parser.add_argument('-m','--mac', help='mac address of terminal, eg -m 00:0d:2e:00:02:81 (no quotes !)', required=False)
    parser.add_argument('-p','--path', help='path to dmm.log.* file', required=False)
    
    args = vars(parser.parse_args())
   
    
    macstring = args['mac']
    
    path = args['path']
    
        
    if path is None:        
        path="../sandbox/dmm.log"
        
    dfStats = dmm.stats_to_dataframe(path)
    #print(dfStats.head())
    dfStats.pipe(hrc.plot_utc,'located','operational')
    dfStats.pipe(hrc.plot_utc,'switch_request','switch_success')
        
    df = dmm.mobile_info_to_dataframe(path, macstring)   
    
    #print(df['mac'].unique())                     
            
    #print(df.head())
    df.to_csv('mobileInfoList.csv')     
    
    #print(str(min(df['dateTimes'])))
    #print(str(max(df['dateTimes'])))
    
    if macstring is None:
        df.pipe(dmm.scatter_on_basemap, title = 'GPS data from terminals')
        df.pipe(dmm.beams_on_basemap, title = 'GPS data from terminals')
    else:
        df.pipe(dmm.scatter_on_basemap, title = ('GPS data from terminal '+ str(macstring)))
        
        # visualise beam switches vs time
        df.pipe(dmm.plot_str_utc,'activebeam')
        
        # visualise lat lon vs time
        df.pipe(hrc.plot_utc,'lat','long')        
        
    
if __name__ == "__main__":
    main(sys.argv)