# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 23:53:29 2018

@author: aro
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import hrclogutils.rtce as rtce



df = rtce.load_rtce_log()

dfpivot = df.pipe(rtce.terminal_averages,'fbAppliedPower','reportedPuSat');
print(dfpivot)