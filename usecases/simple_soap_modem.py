# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 15:34:42 2018

@author: aro
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import argparse
import pandas as pd
from suds.client import Client


def main(argv):   
    
    
    parser = argparse.ArgumentParser(description='script to get DMA stats for an advanced terminal into a python pandas dataframe')
    
    parser.add_argument('-u','--username', help='user name (eg hno)', required=False)
    parser.add_argument('-p','--password', help='eg (D!@l0g', required=False)
    parser.add_argument('-a','--ip', help='CMS IP address, eg 192.168.86.20', required=False)
    parser.add_argument('-t','--terminal', help='modem name eg vno-1.cpe-103', required=False)
    
    args = vars(parser.parse_args())
    
    username = args['username']    
    password = args['password']
    ip = args['ip']
    modem = args['terminal']
    
    
    if username is None:        
        username='hno'
        
    if password is None:        
        password='D!@10g'   

    if ip is None:
        ip = '192.168.80.160'
        
    if modem is None:
        modem = 'vno-1.cpe-103'
        
       
    
    url = 'http://%s/API/V1/soap.asmx?wsdl' % ip
    interface = Client(url, username=username, password=password)
    connection = interface.service.ConnectApp('localhost', username, password, 'test', '?', '?')
    trend = interface.service.GetTrendDataForParameterByName(connection, modem, 'Modem Fwd Es/No', None, "LastDay")
    
    print(len(trend.Data.double))
    
    columns = ['dateTimes','fwd_esno(dB)','rtn_esno(dB)','fwd_throughput(kbps)']
    df = pd.DataFrame(columns=columns)
    df = df.fillna(0) # with 0s rather than NaNs
    
    df['dateTimes'] = trend.Timestamps.dateTime
    df['fwd_esno(dB)'] = trend.Data.double
    
    trend = interface.service.GetTrendDataForParameterByName(connection, modem, 'HRC Es/No', None, "LastDay")
    df['rtn_esno(dB)'] = trend.Data.double
    print(len(trend.Data.double))
    
    print(df.head())
    
    columns = ['dateTimes','fwd_throughput(kbps)','rtn_throughput(kbps)']
    dfT = pd.DataFrame(columns=columns)
    dfT = dfT.fillna(0) # with 0s rather than NaNs
    trend = interface.service.GetTrendDataForParameterByName(connection, modem, 'Modem Total FWD Throughput', None, "LastDay")
    print(len(trend.Data.double))
    print(len(trend.Timestamps.dateTime))
    dfT['dateTimes'] = trend.Timestamps.dateTime    
    dfT['fwd_throughput(kbps)'] = trend.Data.double
    
    trend = interface.service.GetTrendDataForParameterByName(connection, modem, 'Modem Total RTN Throughput', None, "LastDay")
    print(len(trend.Data.double))
    print(len(trend.Timestamps.dateTime))
      
    dfT['rtn_throughput(kbps)'] = trend.Data.double
    print(dfT.head())  
    
    
    
    
if __name__ == "__main__":
    main(sys.argv)