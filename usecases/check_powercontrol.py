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
import argparse


def main(argv):
    
    parser = argparse.ArgumentParser(description='check variuous power control related parameters')
    parser.add_argument('-t','--terminal_id', help='for terminal_123 the required id to be passed as argument is 123', required=False)
    parser.add_argument('-p','--path', help='path to sbc_rtce_monitor.csv', required=False)
    parser.add_argument('-c','--columns', help='path to sbc_rtce_monitor.headers', required=False)

    args = vars(parser.parse_args())
    
    idsubstring = args['terminal_id']
    print(idsubstring)
    path = args['path']
    header_path = args['columns']

    if idsubstring is None:
        idsubstring = "15843"
    
    if path is None:
        path="../tests/sbc_rtce_monitor.csv"
        
    if header_path is None:
        header_path="../tests/sbc_rtce_monitor.headers"
        
    # replace path to appropriate location for your analysis
    df = rtce.load_rtce_log(path, header_path)
    
    # filter on a terminal
    df = df.pipe(rtce.filter_name, idsubstring).pipe(rtce.filter_loggedon)
    
    print(df.head())
    
    print(df.info()) # gives an idea what can be asked to plot
    
    df.pipe(hrc.plot_utc_sof,'Next.TxPSD','txPsdLimit')
    
    df.pipe(hrc.plot_utc_sof,'fbRequestedPower','fbAppliedPower','reportedPuSat')
    
    # TODO: compare reportedPuSat with our own PuSat estimator whenever available
    # TODO: analyse gain stability and gain vs IDU characteristics (incorporate gain based saturation estimation)
    
if __name__ == "__main__":
    main(sys.argv)