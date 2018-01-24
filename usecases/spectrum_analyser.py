# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 23:53:29 2018

 spectrum analyser emulation based on RTCE log file playback
 
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse

import hrclogutils.rtce as rtce




def main(argv):
    
    parser = argparse.ArgumentParser(description='spectrum analyser emulation based on RTCE log file playback')
    
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
        startDateTime="2018-01-17T21:32:07"
        
    if stopDateTime is None:
        stopDateTime="2200-06-15T13:45:30"
        
    df = rtce.load_rtce_log(rtce_path=path,rtce_header_path=header_path)
    df.pipe(rtce.plot_spectrum,"2018-01-17T21:32:07","2018-01-17T21:32:17")
    
    
    
        
    
if __name__ == "__main__":
    main(sys.argv)