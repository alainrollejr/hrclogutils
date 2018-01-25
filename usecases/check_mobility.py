# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 23:53:29 2018

 script to check mobility flows related to a terminal
 
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import pandas as pd
import numpy as np
import datetime
from dateutil.parser import parse

import re


def main(argv):
    
    parser = argparse.ArgumentParser(description='script to check mobility flows related to a terminal')
    parser.add_argument('-t','--terminal_id', help='for terminal_123 the required id to be passed as argument is 123', required=False)
    parser.add_argument('-m','--mac', help='mac address of terminal', required=False)
    parser.add_argument('-p','--path', help='path to dmm.log.* file', required=False)
    
    args = vars(parser.parse_args())
   
    
    idsubstring = args['terminal_id']
    print(idsubstring)
    path = args['path']
    
    
    if idsubstring is None:
        # look at all terminals
        idsubstring = '00:0d:2e:00:02:83'
    
    if path is None:
        path="../sandbox/dmm.log"
        
    with open(path,"r") as f:
        #file_content = f.read().rstrip("\n") # if you don't want end of lines
        file_content = f.read()
        
    print(file_content[0:1000])
    
    """
        first find all mac addresses
    """
    p = re.compile(r'([0-9a-f]{2}(?::[0-9a-f]{2}){5})', re.IGNORECASE)   

    mac_list = re.findall(p, file_content)   
    
    
    mac_list_unique = set(mac_list) #convert list to a set
    print(mac_list_unique)
    print(str(len(mac_list_unique)) + ' unique mac addresses found')
    
    
    """
        Now search for all GetMobileInfoList calls and map that to a pandas dataframe
        
    18/01/25-00:23:26.613 [D] [Mobility.DMM.DmmCtl ] Response: "GetMobileInfoList": { mobiles={ 00:0d:2e:00:02:81={ status=state=operational/located; active-beam='BEAM_AMC15_W01_0001'; switching-beam=<nil>; position-timeout={ timestamp=16127066be0; count=2 }; switch-success={ timestamp=0; count=0 }; switch-timeout={ timestamp=0; count=0 }; mobility-info=timestamp=1612ab27741; longitude=-117.668; latitude=33.66; altitude=<nil>; skew-angle=<nil>; heading=<nil>; speed=<nil>; yaw=<nil>; roll=<nil>; noTxExclusionZone={ start-time=16129c74994 milliseconds; end-time=16129c74c48 milliseconds }; beams={ 'BEAM_AMC15_W01_0001'={ requested=Unlocked; reported=Unlocked };'BEAM_STM8_W01_0005'={ requested=Locked; reported=Locked } }; control=target-beam=<nil>; enforce-aibs={ false } };00:0d:2e:00:02:82={ status=state=operational/located; active-beam='BEAM_AMC15_W01_0001'; switching-beam=<nil>; position-timeout={ timestamp=16127066978; count=5 }; switch-success={ timestamp=0; count=0 }; switch-timeout={ timestamp=0; count=0 }; mobility-info=timestamp=1612ab274ee; longitude=-117.669; latitude=33.6; altitude=<nil>; skew-angle=<nil>; heading=<nil>; speed=<nil>; yaw=<nil>; roll=<nil>; noTxExclusionZone={ start-time=161270e7c4b milliseconds; end-time=161270e84fd milliseconds }; beams={ 'BEAM_AMC15_W01_0001'={ requested=Unlocked; reported=Unlocked } }; control=target-beam=<nil>; enforce-aibs={ false } };00:0d:2e:00:02:83={ status=state=operational/located; active-beam='BEAM_AMC15_W01_0001'; switching-beam=<nil>; position-timeout={ timestamp=0; count=0 }; switch-success={ timestamp=0; count=0 }; switch-timeout={ timestamp=0; count=0 }; mobility-info=timestamp=1612ab28f8b; longitude=-117.67; latitude=33.66; altitude=<nil>; skew-angle=<nil>; heading=<nil>; speed=<nil>; yaw=<nil>; roll=<nil>; noTxExclusionZone={ start-time=16129f6cb70 milliseconds; end-time=16129f6cd05 milliseconds }; beams={ 'BEAM_AMC15_W01_0001'={ requested=Unlocked; reported=Unlocked } }; control=target-beam=<nil>; enforce-aibs={ false } };00:0d:2e:00:0...0012'={ requested=Locked; reported=Locked } }; control=target-beam=<nil>; enforce-aibs={ false } } } }
    18/01/25-00:23:27.212 [D] [Mobility.DMM.DmmCtl ] Request "GetStatistics": {  }
    """
    

    columns = ['dateTime','mac', 'lat', 'long','located','activebeam']
    df = pd.DataFrame(columns=columns)
    df = df.fillna(0) # with 0s rather than NaNs
    i = 1
    for line in file_content.splitlines():
        if "Response: \"GetMobileInfoList\"" in line:
            date = datetime.datetime.strptime(line[0:20],"%y/%m/%d-%H:%M:%S.%f")
            #date = parse(line[0:20]) 
            print(line)
            print(str(date))
            i = i+1
            
            if (i > 10):
                break
            
    print(df.head())
        
        
    
        
    
if __name__ == "__main__":
    main(sys.argv)