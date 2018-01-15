# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import hrclogutils.basic as hrc

# replace path to appropriate location for your analysis
df = hrc.load_rtce_log("../tests/sbc_rtce_monitor.csv","../tests/sbc_rtce_monitor.headers")


# filter on a terminal, replace terminal id according to your needs 
terminal_id = '15843'
df = df.pipe(hrc.filter_name,terminal_id).pipe(hrc.filter_loggedon)

print(df.head())

print(df.info()) # gives an idea what can be asked to plot

df.pipe(hrc.plot_utc_sof,'Next.TxPSD','txPsdLimit')

df.pipe(hrc.plot_utc_sof,'fbRequestedPower','fbAppliedPower','reportedPuSat')