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
import hrclogutils.basic as hrc


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
    
    
    columns = ['dateTimes','fwd_esno(dB)']
    df_fwd = pd.DataFrame(columns=columns)
    df_fwd = df_fwd.fillna(0) # with 0s rather than NaNs
    
    trend = interface.service.GetTrendDataForParameterByName(connection, modem, 'Modem Fwd Es/No', None, "LastDay")    
    print(len(trend.Data.double))
    df_fwd['dateTimes'] = trend.Timestamps.dateTime
    df_fwd['fwd_esno(dB)'] = trend.Data.double
    print(df_fwd.head())
    df_fwd.pipe(hrc.plot_utc,'fwd_esno(dB)')
    
    columns = ['dateTimes','rtn_cond(dB)']
    df_rtn = pd.DataFrame(columns=columns)
    df_rtn = df_rtn.fillna(0) # with 0s rather than NaNs
    trend = interface.service.GetTrendDataForParameterByName(connection, modem, 'HRC CoND', None, "LastDay")
    df_rtn['dateTimes'] = trend.Timestamps.dateTime
    df_rtn['rtn_cond(dB)'] = trend.Data.double
    print(len(trend.Data.double))    
    df_rtn.pipe(hrc.plot_utc,'rtn_cond(dB)')
    
    
    columns = ['dateTimes','fwd_throughput(kbps)']
    df_fwd_T = pd.DataFrame(columns=columns)
    df_fwd_T = df_fwd_T.fillna(0) # with 0s rather than NaNs
    trend = interface.service.GetTrendDataForParameterByName(connection, modem, 'Modem Total FWD Throughput', None, "LastDay")
    print(len(trend.Data.double))
    print(len(trend.Timestamps.dateTime))
    df_fwd_T['dateTimes'] = trend.Timestamps.dateTime    
    df_fwd_T['fwd_throughput(kbps)'] = trend.Data.double
    print(df_fwd_T.head())  
    df_fwd_T.pipe(hrc.plot_utc,'fwd_throughput(kbps)')
    
    columns = ['dateTimes','rtn_throughput(kbps)']
    df_rtn_T = pd.DataFrame(columns=columns)
    df_rtn_T = df_rtn_T.fillna(0) # with 0s rather than NaNs
    trend = interface.service.GetTrendDataForParameterByName(connection, modem, 'Modem Total RTN Throughput', None, "LastDay")
    print(len(trend.Data.double))
    print(len(trend.Timestamps.dateTime))
    df_rtn_T['dateTimes'] = trend.Timestamps.dateTime   
    df_rtn_T['rtn_throughput(kbps)'] = trend.Data.double
    print(df_rtn_T.head()) 
   
    df_rtn_T.pipe(hrc.plot_utc,'rtn_throughput(kbps)')
    
    
    
    
if __name__ == "__main__":
    main(sys.argv)