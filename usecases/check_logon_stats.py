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

import hrclogutils.basic as hrc
import hrclogutils.rtce as rtce



def main(argv):
    if len(argv)==3:
        df = rtce.load_rtce_log(argv[1],argv[2])
    else:
        df = rtce.load_rtce_log(argv[1], "../tests/sbc_rtce_monitor.headers")
    
    
    # filter to display terminals only when they are logging on
    df = df.pipe(rtce.filter_loggingon)
    df = df.reset_index()
    
    # print the logon attempts vs time, for all terminal id's
    df.pipe(hrc.plot_utc_sof,'id')
    
    id_list = df['id'].unique()
    print(str(len(id_list)) +  " unique terminal id\'s in log:")
    print(id_list)


if __name__ == "__main__":
    main(sys.argv)


