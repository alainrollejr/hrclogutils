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



def main(argv):   
    
    
    parser = argparse.ArgumentParser(description='script to get all terminals from NMS')
    
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
        url= 'http://192.168.86.20/rest/modem/'
    else:
        url = url + 'rest/modem'
        print(url)
        
    
   
    r = requests.get(url, auth=(user, password))
  
    print(r.text)
    
if __name__ == "__main__":
    main(sys.argv)