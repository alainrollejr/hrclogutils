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

import argparse

def main(argv):
    
    parser = argparse.ArgumentParser(description='script to check performance of a satnet (efficiency, esno, etc)')
    
    parser.add_argument('-p','--path', help='path to sbc_carrier_tracking_monitor.csv', required=False)
    parser.add_argument('-c','--columns', help='path to sbc_carrier_tracking_monitor.headers', required=False)

    args = vars(parser.parse_args())
    path = args['path']
    header_path = args['columns']
    
    if path is None:
        path="../tests/sbc_carrier_tracking_monitor.csv"
        
    if header_path is None:
        header_path="../tests/sbc_carrier_tracking_monitor.headers"
    
    
    df = carrier.load_carrier_log(path, header_path)

    #print(df.head())
    dfpivot = df.pipe(carrier.terminal_averages,'curEsNo(dB)','efficiency(bits/symbol)','allocatedRate(bits/s)','chiprate(Bd)');
    print(dfpivot.head())
    
    # pie chart that shows average consumption of bandwidth by all terminals
    dfpivot.pipe(hrc.plot_pie,'chiprate(Bd)','terminal')
    
    # bar chart that shows average efficiency
    dfpivot.pipe(hrc.plot_bar,'efficiency(bits/symbol)','terminal')
    
    
    

if __name__ == "__main__":
    main(sys.argv)
    