# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 23:53:29 2018

@author: aro
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import hrclogutils.basic as hrc
import hrclogutils.carrier as carrier

def main(argv):
    if len(argv)==3:
        df = carrier.load_carrier_log(argv[1],argv[2])
    elif len(argv)==2:
        df = carrier.load_carrier_log(argv[1], "../tests/sbc_carrier_tracking_monitor.headers")
    elif len(argv)==1:
        df = carrier.load_carrier_log("../tests/sbc_carrier_tracking_monitor.csv", "../tests/sbc_carrier_tracking_monitor.headers")

    print(df.head())
    dfpivot = df.pipe(carrier.terminal_averages,'curEsNo(dB)','efficiency(bits/symbol)','allocatedRate(bits/s)','chiprate(Bd)');
    print(dfpivot.head())
    
    # pie chart that shows average consumption of bandwidth by all terminals
    dfpivot.pipe(hrc.plot_pie,'chiprate(Bd)','terminal')
    
    # bar chart that shows average efficiency
    dfpivot.pipe(hrc.plot_bar,'efficiency(bits/symbol)','terminal')
    
    
    

if __name__ == "__main__":
    main(sys.argv)
    