# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import hrclogutils.basic as hrc

df = hrc.load_rtce_log()


# filter on terminal_15843, when he is logged on
df = df.pipe(hrc.filter_name,'15843').pipe(hrc.filter_loggedon)

print(df.head())

print(df.info()) # gives idea what can be asked to plot


df.pipe(hrc.plot_sof,'txPsdLimit')

df.pipe(hrc.plot_utc,'Next.TxPSD','txPsdLimit')

df.pipe(hrc.plot_utc_sof,'Next.TxPSD','txPsdLimit')