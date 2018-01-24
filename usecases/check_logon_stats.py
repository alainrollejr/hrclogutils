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
    args = vars(parser.parse_args())
   
    
   
    path = args['path']
    header_path = args['columns']
 
    
   
    if path is None:
        path="./sbc_rtce_monitor.csv"
        
    if header_path is None:
        header_path="../tests/sbc_rtce_monitor.headers"
    
    
    
        
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


