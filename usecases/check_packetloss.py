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
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import hrclogutils.carrier as carrier


def main(argv):
    if len(argv)==3:
        carrier.packet_error_analysis(idsubstring=argv[1],path=argv[2],header_path="../tests/sbc_carrier_tracking_monitor.headers")
       
    elif len(argv)==1:
        idsubstring = '15843'
        carrier.packet_error_analysis(idsubstring,startDateTime="2018-01-15T11:23:59", path="../tests/sbc_carrier_tracking_monitor.csv", header_path="../tests/sbc_carrier_tracking_monitor.headers")

if __name__ == "__main__":
    main(sys.argv)