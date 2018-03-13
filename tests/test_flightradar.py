# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 11:54:16 2018

@author: aro

    prerequisite is having run
    "pip install pyflightdata"

"""
import json
from pyflightdata import FlightData

api=FlightData()

max_nr_entries = 100
r = api.get_history_by_tail_number('N812UA')[-max_nr_entries:]

m = json.dumps(r)
rjson = json.loads(m)

#print(rjson)
for item in rjson:
    # first items are most recent
    print('from :' + str(item["airport"]["origin"]["name"]))
    print('to: ' + str(item["airport"]["destination"]["name"]))
    print('status: ' + str(item["status"]["text"]))
    print(item["time"]["real"])
    print("\n")
    
