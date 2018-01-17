# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import hrclogutils.basic as hrc
import hrclogutils.rtce as rtce

# replace path to appropriate location for your analysis
df = rtce.load_rtce_log("./sbc_rtce_monitor.csv","../tests/sbc_rtce_monitor.headers")


# filter to display terminals only when they are logging on
df = df.pipe(rtce.filter_loggingon)
df = df.reset_index()

# print the logon attempts vs time, for all terminal id's
df.pipe(hrc.plot_utc_sof,'id')

id_list = df['id'].unique()
print(str(len(id_list)) +  " unique id\'s in log:")
print(id_list)



