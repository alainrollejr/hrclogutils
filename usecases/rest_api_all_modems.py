# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 15:34:42 2018

@author: aro
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
import argparse
import pandas as pd



def main(argv):   
    
    
    parser = argparse.ArgumentParser(description='script to get all terminals from NMS, put into pandas dataframe')
    
    parser.add_argument('-u','--user', help='user name (eg hno)', required=False)
    parser.add_argument('-p','--password', help='eg (D!@l0g', required=False)
    parser.add_argument('-a','--url', help='url, eg http://192.168.86.20/', required=False)
    
    args = vars(parser.parse_args())
    
    user = args['user']    
    password = args['password']
    url = args['url']
    
    
    if user is None:        
        user='hno'
        
    if password is None:        
        password='D!@10g'   

    if url is None:
        url= 'http://192.168.80.160/'
        
    
    urlstr = url + 'rest/modem?limit=1000' #assumed never more than 1000 terminals
    print(urlstr)
        
    
    
    r = requests.get(urlstr, auth=(user, password))    
    rjson = r.json()  
    
 
    # the dataframe column headers
    columns = ['mac', 'systemId','name','roaming', 'locked', 'attachmentType', 'attachmentProfile', 'satnet']
    df = pd.DataFrame(columns=columns)
    df = df.fillna(0) # with 0s rather than NaNs
    
    for el in rjson: # each element is a dict(ionary)        
        #print(el.keys()) # get all keys that you can query
        
        attach = el["attachment"]
        typestr = attach["type"]
        if "DYNAMIC" in typestr:            
            print(attach["attachmentProfileId"]["name"])
        
            row=pd.Series([el["macAddress"], el["id"]["systemId"],
                           el["id"]["name"],el["beamRoamingEnabled"],
                           el["locked"],attach["type"], attach["attachmentProfileId"]["name"], ""],columns)
        else:
            row=pd.Series([el["macAddress"], el["id"]["systemId"],
                           el["id"]["name"],el["beamRoamingEnabled"],
                           el["locked"],attach["type"], "", attach["satelliteNetworkId"]["name"]],columns)
    
        df = df.append([row],ignore_index=True)
        
        
    print(df)
    df.to_csv('modem_list.csv')
    print(str(len(df.index)) + ' provisioned terminals found')
    dfUnlocked = df[df["locked"]==False]
    dfUnlocked = dfUnlocked.reset_index(drop=True)
    print(str(len(dfUnlocked.index)) + ' unlocked terminals found')
    
    urlstr = url + 'rest/attachment-profile'
    print(urlstr)
    r = requests.get(urlstr, auth=(user, password))    
    rjson = r.json() 
    
    # now get the relationship between attachment profiles and satnets
    
    attach_columns = ['attachmentProfile', 'satnet']
    dfAttachments = pd.DataFrame(columns=attach_columns)
    
    for el in rjson:
        print(el['id']['name'])
        for subel in el["attachments"]:
            print(subel["satelliteNetworkId"]["name"])
            row = pd.Series([el['id']['name'],subel["satelliteNetworkId"]["name"]], attach_columns )
            dfAttachments = dfAttachments.append([row],ignore_index=True)
    
    print(dfAttachments)
    dfAttachments.to_csv('attachment_profiles.csv')
   
    
    
    
    
        
    
if __name__ == "__main__":
    main(sys.argv)