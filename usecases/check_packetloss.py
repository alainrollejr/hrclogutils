# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 23:53:29 2018

 script to check on packetloss for a terminal, and to investigate to what the
 packet loss potentially correlates.
 
 Execute from CLI as follows:

 python check_packetloss.py 15843 ../tests/sbc_carrier_tracking_monitor.csv
 
 in Spyder IDU %run check_packetloss.py 15843 ../tests/sbc_carrier_tracking_monitor.csv
 
"""
import os
import sys
import argparse

import hrclogutils.carrier as carrier

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))






def main(argv):
    
    parser = argparse.ArgumentParser(description='script to check on packetloss for a terminal, and to investigate to what the  packet loss potentially correlates')
    parser.add_argument('-t','--terminal_id', help='for terminal_123 the required id to be passed as argument is 123', required=True)
    parser.add_argument('-p','--path', help='path to sbc_carrier_tracking_monitor.csv', required=False)
    parser.add_argument('-c','--columns', help='path to sbc_carrier_tracking_monitor.headers', required=False)
    parser.add_argument('-b','--beginTime', help='begin time eg 2018-01-15T11:23:59', required=False)
    parser.add_argument('-e','--endTime', help='end time eg 2018-01-15T12:23:59', required=False)
    args = vars(parser.parse_args())
   
    
    idsubstring = args['terminal_id']
    print(idsubstring)
    path = args['path']
    header_path = args['columns']
    startDateTime = args['beginTime']
    stopDateTime = args['endTime']
    
    if idsubstring is None:
        idsubstring = "15843"
    
    if path is None:
        path="../tests/sbc_carrier_tracking_monitor.csv"
        
    if header_path is None:
        header_path="../tests/sbc_carrier_tracking_monitor.headers"
        
    if startDateTime is None:
        startDateTime="1977-06-02T13:45:30"
        
    if stopDateTime is None:
        stopDateTime="2200-06-15T13:45:30"
        
    
if __name__ == "__main__":
    main(sys.argv)