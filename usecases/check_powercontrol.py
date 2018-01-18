# -*- coding: utf-8 -*-
"""
    This script visualises the power control action for a certain terminal
    
    To run it from cli:
        
        python check_powercontrol.py terminal_id path_to_rtce_csv
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import hrclogutils.basic as hrc
import hrclogutils.rtce as rtce


def main(argv):
    if len(argv)==3:
        terminal_id = argv[1] # as a number so terminal_123 -> terminal_id = 123
        path = argv[2]
    elif len(argv)==1:
        terminal_id = '15843'
        path = "../tests/sbc_rtce_monitor.csv"
        
    # replace path to appropriate location for your analysis
    df = rtce.load_rtce_log(path,"../tests/sbc_rtce_monitor.headers")
    
    # filter on a terminal
    df = df.pipe(rtce.filter_name,terminal_id).pipe(rtce.filter_loggedon)
    
    print(df.head())
    
    print(df.info()) # gives an idea what can be asked to plot
    
    df.pipe(hrc.plot_utc_sof,'Next.TxPSD','txPsdLimit')
    
    df.pipe(hrc.plot_utc_sof,'fbRequestedPower','fbAppliedPower','reportedPuSat')
    
if __name__ == "__main__":
    main(sys.argv)