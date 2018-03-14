# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 21:28:37 2018

@author: aro
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import hrclogutils.dmm as dmm
import hrclogutils.basic as hrc
import pandas as pd
import matplotlib.pyplot as plt

import json
from datetime import datetime
from pyflightdata import FlightData


def get_flightradar_info_for_mac(mac,path_to_modem_list):
    modem_df = pd.read_csv(path_to_modem_list)  
    row = modem_df[modem_df['mac']==mac]
    tail = row.iloc[0]['tail']
    print('tail = ' + str(tail))
    return tail

def main(argv):
    
    pd.options.mode.chained_assignment = None  # default='warn'
    
    parser = argparse.ArgumentParser(description='script to check flight radar data for a terminal')
    
    parser.add_argument('-m','--mac', help='mac address of terminal, eg -m 00:0d:2e:00:02:81 (no quotes !)', required=False)
    parser.add_argument('-t','--tail', help='tail nr of aircraft eg -t N482UA (no quotes !)', required=False)
    parser.add_argument('-p','--path', help='path to dmm.log.* file', required=False)
    parser.add_argument('-l','--modemlist', help='path to modem_list.csv, which can be fetched via rest_api_all_modems.py', required=True)
    
    args = vars(parser.parse_args())
   
    path_to_modem_list = args['modemlist']
    mac = args['mac']
    
    if mac is None:
        tail = args['tail']        
        modem_df = pd.read_csv(path_to_modem_list)  
        row = modem_df[modem_df['tail']==tail]
        mac = row.iloc[0]['mac']
    
    path = args['path']
    
    
    columns = ['dateTimes','mac','operational','located','event','airport']
    dfChanges = dmm.changes_to_dataframe(path, mac)
    
    #df = dmm.mobile_info_to_dataframe(path, mac)
    
    
    
    tail =get_flightradar_info_for_mac(mac,path_to_modem_list)

    api=FlightData()
    
    max_nr_entries = 100
    r = api.get_history_by_tail_number(tail)[-max_nr_entries:]
    
    m = json.dumps(r)
    rjson = json.loads(m)
    
    #print(rjson)
    
    for item in rjson:
        # first items are most recent    
        status = item["status"]["generic"]["status"]["text"]
        
        if status == "landed": # everything else is scheduled or estimated
            from_airport = str(item["airport"]["origin"]["name"])
            to_airport = str(item["airport"]["destination"]["name"])
            
            
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
                row=pd.Series([departure_utc, mac,'','',"departure",from_airport],columns)
                dfChanges = dfChanges.append([row],ignore_index=True)
                #print("departure " + str(departure_utc))
                
            if arrival_known:
                row=pd.Series([arrival_utc, mac,'','',"arrival",to_airport],columns)
                dfChanges = dfChanges.append([row],ignore_index=True)
                #print("arrival " + str(arrival_utc))
            
            #print("\n")
            
            
    # TODO: add beam switch events
    # 18/03/11-23:21:54.618 [I] [ility.DMM.Mobile.Fsm] 00:0d:2e:00:06:74 performs switch to beam 'BEAM_AMZ2_W02_0003' (active-beam: 'BEAM_AMC15_W06_0027')
    
 
    dfMutes = dmm.txmutes_to_dataframe(path, mac)
    dfBeams = dmm.beam_info_to_dataframe(path, mac)    
    dfSLA = pd.concat([dfMutes,dfChanges,dfBeams])
    
    dfSLA = dfSLA.sort_values(by='dateTimes',ascending=True)
    dfSLA.to_csv('input_for_sla.csv', index=False)
        
    
    
       
    
if __name__ == "__main__":
    main(sys.argv)
        

