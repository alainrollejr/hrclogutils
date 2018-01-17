# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 23:53:29 2018

@author: aro
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import hrclogutils.carrier as carrier



df = carrier.load_carrier_log(path="../tests/sbc_carrier_tracking_monitor.csv",header_path="../tests/sbc_carrier_tracking_monitor.headers")
dfpivot = df.pipe(carrier.terminal_minmax,'curEsNo(dB)','modcod','spreadingFactor');
print(dfpivot)