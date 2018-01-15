# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 23:53:29 2018

@author: aro
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import hrclogutils.basic as hrc
import hrclogutils.rtce as rtce

df = rtce.load_rtce_log()


# filter on terminal_15843, in a certain time episode
df = df.pipe(rtce.filter_name,'15843').pipe(hrc.filter_utc,startDateTime="2018-01-08T01:42:39",stopDateTime="2018-01-08T01:43:14")

print(df.head())
print(df.tail())

print(df.info()) # gives idea what can be asked to plot