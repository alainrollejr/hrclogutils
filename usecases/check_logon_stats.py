# -*- coding: utf-8 -*-
"""
 Visualises logon carousel
 
 python check_logon_stats path_to_rtce_csv (optional: path to rtce headers file)
 
 in spyder IDE:
     %run check_logon_stats path_to_rtce_csv (optional: path to rtce headers file)
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse

import hrclogutils.basic as hrc
import hrclogutils.rtce as rtce



def main(argv):
    
    parser = argparse.ArgumentParser(description='get overview of logon attempts for terminals')
    
    parser.add_argument('-p','--path', help='path to sbc_rtce_monitor.csv', required=False)
    parser.add_argument('-c','--columns', help='path to sbc_rtce_monitor.headers', required=False)
    parser.add_argument('-b','--beginTime', help='begin time eg 2018-01-15T11:23:59', required=False)
    parser.add_argument('-e','--endTime', help='end time eg 2018-01-15T12:23:59', required=False)
    args = vars(parser.parse_args())
   
    
   
    path = args['path']
    header_path = args['columns']
    startDateTime = args['beginTime']
    stopDateTime = args['endTime']
    
   
    if path is None:
        path="./sbc_rtce_monitor.csv"
        
    if header_path is None:
        header_path="../tests/sbc_rtce_monitor.headers"
        
    if startDateTime is None:
        startDateTime="1977-06-02T13:45:30"
        
    if stopDateTime is None:
        stopDateTime="2200-06-15T13:45:30"
    
    
        
    df = rtce.load_rtce_log(path, header_path)
    
    
    # filter to display terminals only when they are logging on
    df = df.pipe(rtce.filter_loggingon)
    df = df.reset_index()
    
    # print the logon attempts vs time, for all terminal id's
    df.pipe(hrc.plot_str_utc_sof,'name')
    
    id_list = df['id'].unique()
    print(str(len(id_list)) +  " unique terminal id\'s in log:")
    print(id_list)    
   


if __name__ == "__main__":
    main(sys.argv)


