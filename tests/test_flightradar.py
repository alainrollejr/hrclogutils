# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 11:54:16 2018

@author: aro

    prerequisite is having run
    "pip install pyflightdata"

"""
import json
from datetime import datetime
from pyflightdata import FlightData

api=FlightData()

max_nr_entries = 20
r = api.get_history_by_tail_number('N812UA')[-max_nr_entries:]

m = json.dumps(r)
rjson = json.loads(m)

#print(rjson)

for item in rjson:
    # first items are most recent    
    status = item["status"]["generic"]["status"]["text"]
    
    if status == "landed": # everything else is scheduled or estimated
        print('from :' + str(item["airport"]["origin"]["name"]))
        print('to: ' + str(item["airport"]["destination"]["name"]))
        print('status: ' + str(status))
        
        try:
            departure_utc = datetime.utcfromtimestamp(int(item["time"]["real"]["departure"]))
            departure_known = True
        except:
            departure_known = False
            
        try:
            arrival_utc = datetime.utcfromtimestamp(int(item["time"]["real"]["arrival"]))
            arrival_known = True
        except:
            arrival_known = False
        
        if departure_known:
            print("departure " + str(departure_utc))
            
        if arrival_known:
            print("arrival " + str(arrival_utc))
        
        print("\n")
    
