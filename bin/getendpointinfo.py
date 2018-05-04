#!/usr/bin/python

# Python script to gather public and private IP info from Windows (and other)
# endpoints for accurate IP mapping. Index data in Splunk and build lookups
#
# brodsky@splunk.com 5-3-2018

import sys
import datetime
import socket
import re
import uuid
import requests
import json

from dateutil.tz import tzlocal 

# parse time and timezone
runtime = datetime.datetime.now()
runtimef = runtime.strftime("%Y-%m-%d %H:%M:%S")
runtimez = datetime.datetime.now(tzlocal()).tzname()

# get local hostname and local IP address and local MAC
localhostname = socket.gethostname()
localip = socket.gethostbyname(localhostname)
localmac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))

# reach out to ipinfo and...
# get public IP address info from ipinfo
getipinfourl = 'http://ipinfo.io/json'
try:
   ipinfodata=requests.get(getipinfourl).json()
except requests.exceptions.RequestException as e:
   error = e 
   print ("%s error condition: %s" % (runtimef,e))
   sys.exit(1)

publicip=ipinfodata["ip"]
ip_loc=ipinfodata["loc"]
ip_hostname=ipinfodata["hostname"]
ip_org=ipinfodata["org"]
ip_postal=ipinfodata["postal"]

# print output
print ("%s hosttz=\"%s\" hostname=\"%s\" local_ip=\"%s\" public_ip=\"%s\" localmac=\"%s\" ip_location=\"%s\" ip_hostname=\"%s\" ip_org=\"%s\" ip_postal=\"%s\"" % (runtimef,runtimez,localhostname,localip,publicip,localmac,ip_loc,ip_hostname,ip_org,ip_postal)) 


