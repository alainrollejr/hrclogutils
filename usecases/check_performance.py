# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 23:53:29 2018

@author: aro
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import hrclogutils.carrier as carrier

def main(argv):
    if len(argv)==3:
        df = carrier.load_carrier_log(argv[1],argv[2])
    else:
        df = carrier.load_carrier_log(argv[1], "../tests/sbc_carrier_tracking_monitor.headers")


    dfpivot = df.pipe(carrier.terminal_minmax,'curEsNo(dB)','modcod','spreadingFactor');
    print(dfpivot)
    

if __name__ == "__main__":
    main(sys.argv)
    