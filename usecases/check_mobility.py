# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 23:53:29 2018

 script to check mobility flows related to a terminal
 
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse


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
        file_content = f.read().rstrip("\n")
        
    print(file_content[0:100])
    
    
    p = re.compile(r'([0-9a-f]{2}(?::[0-9a-f]{2}){5})', re.IGNORECASE)
    

    mac_list = re.findall(p, file_content)   
    
    
    mac_list_unique = set(mac_list) #convert list to a set
    print(mac_list_unique)
    print(str(len(mac_list_unique)) + ' unique mac addresses found')
    
        
    
if __name__ == "__main__":
    main(sys.argv)