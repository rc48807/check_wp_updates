#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script to check the status of update of wordpress, based on information taken from
the API https://api.wordpress.org/core/version-check/1.7/ and site https://wordpresss.org

Creation date: 30/10/2016
Date last updated: 19/03/2017

Nagios check_wp_update plugin
* 
* License: GPL
* Copyright (c) 2016 DI-FCUL
* 
* Description:
* 
* This file contains the check_wp_update plugin
* 
* Use the nrpe program to check update information for wordpress in remote host.
* 
* 
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
* 
* You should have received a copy of the GNU General Public License
* along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys
import urllib.request
import re
import urllib
from optparse import OptionParser
import json
import os

__author__ = "\nAuthor: Raimundo Henrique da Silva Chipongue\nE-mail: fc48807@alunos.fc.ul.pt, chipongue1@gmail.com\nInstitution: Faculty of Science of the University of Lisbon\n"
__version__= "1.0.0"

# define exit codes
ExitOK = 0
ExitWarning = 1
ExitCritical = 2
ExitUnknown = 3

def check_connectivity():
    '''
    Check if the internet conection is up
    '''
    try:
        urllib.request.urlopen('https://wordpress.org/download', timeout=1)
        return True
    except urllib.request.URLError:
        return False
  
def version(opts):   
    if check_connectivity():
        wp_installed_version_path = opts.path         
        def installed_wp_version():
            '''
            Get the installed WordPress version
            '''
            for line in open(wp_installed_version_path):
                if "wp_version =" in line:
                    version_number = re.search('[-+]?\d+[\.]?\d*[\.]?\d*', line)
                    if version_number:
                        installed_version = str(version_number.group())
                        installed_version = installed_version.replace("-", "")
            return(installed_version)

        installed_version = installed_wp_version()
        def current_wp_version():
            '''
            Get the latest stable version WordPress
            '''
            api_path = "https://api.wordpress.org/core/version-check/1.7/"
            result = os.popen("curl -s %s "%api_path).read()

            try:
                latest = json.loads(result)["offers"][0]
                current_version = (latest["version"])
            except ValueError:
                return False
            
            if current_version == installed_version:
                print('The latest stable version WordPress %s available in wordpress.org is installed'%current_version)
                sys.exit(ExitOK)
            else:
                print('Version outdated, has installed WordPress %s, but is available in wordpress.org the version %s' %(installed_version, current_version))
                sys.exit(ExitCritical)
                  
        wp_current_version = current_wp_version()
        if not wp_current_version:
            '''
            Get the latest stable version WordPress
            '''
            wp_current_version_url = "https://wordpress.org/download"
            values = {'s':'wordpress', 'submit':'search'}
            data = urllib.parse.urlencode(values)
            data = data.encode('utf-8')
            req = urllib.request.Request(wp_current_version_url, data)
            resp = urllib.request.urlopen(req)
            respData = resp.read()
            text_version = re.findall(r'<strong>(.*?)</strong>', str(respData))
            for eachP in text_version:
                version_number = re.search('[-+]?\d+[\.]?\d*[\.]?\d*', eachP)                
                if version_number:
                    current_version = str(version_number.group())
                    current_version = current_version.replace("-", "")
                    if current_version == installed_version:
                        print('The latest stable version WordPress %s available in wordpress.org is installed' %current_version)
                        sys.exit(ExitOK)
                    else:
                        print('Version outdated, has installed WordPress %s, but is available in wordpress.org the version %s' %(installed_version, current_version))
                        sys.exit(ExitCritical)
         
            print('Error, Connot read the current stable WordPress Version')
            sys.exit(ExitUnknown)

    else:
        print('Error, check you internet connection')
        sys.exit(ExitUnknown)
       
def main():
    parser = OptionParser("usage: %prog [options] arg1. \nEx.: %prog -p /var/www/html/wp-includes/version.php" )
    parser.add_option("-p", "--path", dest="path",
                      help="specify full path of version.php in wp folder installation", type="string")
    parser.add_option("-V","--version", action="store_true", dest="version", help="This option show the current version number of the program and exit")
    parser.add_option("-A","--author", action="store_true", dest="author", help="This option show author information and exit")
    (opts, args) = parser.parse_args()
    
    
    if opts.author:
        print(__author__)
        sys.exit()
    if opts.version:
        print("check_wp-update.py %s"%__version__)
        sys.exit()

    if not opts.path:
        parser.error("This program requires at least one argument") 
        sys.exit(ExitUnknown)

    if opts.path:
        if not os.path.exists(opts.path):
            parser.error("Please, this program requires to specify a valid path file.")
        else:
             version(opts)
    else:
        parser.error("Please, this program requires to specify a valid path path file.")

   

if __name__ == '__main__':
    main()

