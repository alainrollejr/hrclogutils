# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 15:42:42 2018

@author: aro
"""
import numpy as np
import hrclogutils.basic as hrc

# load the rtce log (Real Time Channel Estimator log) into a python pandas dataframe
def load_rtce_log(rtce_path="./sbc_rtce_monitor.csv",rtce_header_path="./sbc_rtce_monitor.headers"):
    df = hrc.load_csv_log(rtce_path,rtce_header_path)
    # enhance with some derived columns
    #df['SCH.allocatedRate'] =  df['SCH.Sr'].values.astype(np.float) * df['SCH.Mc'].values.astype(np.float)
    return df;


# filter on terminal id, id should be the 'xyz' string found in 'terminal_xyz'
def filter_name(df, idsubstring): 
    return df[df['name'].str.contains(idsubstring)]

# filter on episodes where terminals are logged on or at least sending power above noise. 
def filter_loggedon(df):
    return df[df['MCD.Signal'].str.contains('Ok')]	