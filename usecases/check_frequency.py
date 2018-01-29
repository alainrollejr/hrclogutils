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
import pandas as pd

import argparse

def main(argv):
    
    parser = argparse.ArgumentParser(description='script to check performance of a satnet (efficiency, esno, etc)')
    
    parser.add_argument('-p','--path', help='path to sbc_carrier_tracking_monitor.csv', required=False)
    parser.add_argument('-c','--columns', help='path to sbc_carrier_tracking_monitor.headers', required=False)

    args = vars(parser.parse_args())
    path = args['path']
    header_path = args['columns']
    
    if path is None:
        path="../sandbox/sbc_carrier_tracking_monitor.csv"
        
    if header_path is None:
        header_path="../tests/sbc_carrier_tracking_monitor.headers"
    
    
    df = carrier.load_carrier_log(path, header_path)

    df = df.pipe(hrc.reduce,'dateTimes','sof','terminal','curFreqOffset(Hz)')
    
    
    
    
    print(df.head())
    
    #print(df['dateTimes'].dt.round('S'))
    
    dfPivot = pd.pivot_table(df,index=["sof","dateTimes"],columns=["terminal"], values=['curFreqOffset(Hz)'])
    
    print(dfPivot.head())

if __name__ == "__main__":
    main(sys.argv)
    