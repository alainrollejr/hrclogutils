# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 23:53:29 2018

@author: aro
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import hrclogutils.carrier as carrier

idsubstring = '15843'

carrier.packet_error_analysis(idsubstring,startDateTime="2018-01-15T11:23:59")

# pivot table test
df = carrier.load_carrier_log()
dfpivot = df.pipe(carrier.terminal_averages,'curEsNo(dB)','curFreqOffset(Hz)');
print(dfpivot)

df = carrier.load_carrier_log()
dfpivot = df.pipe(carrier.terminal_minmax,'curEsNo(dB)','modcod','spreadingFactor','curFreqOffset(Hz)');
print(dfpivot)