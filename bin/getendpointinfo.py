#!/usr/bin/python

# Python script to gather public and private IP info from Windows (and other)
# endpoints for accurate IP mapping. Index data in Splunk and build lookups
#
# brodsky@splunk.com 5-3-2018
# 1.3 - checks for existence of keys in dict - turns out sometimes all keys are not returned
# by ipinfo
# 1.2 - writes temp file to /tmp on *nix/mac platform. also uses "platform"
# instead of "socket" because of permissions issue. 
# 1.1 - heartbeat and logic functions - only sends info if either new IP is seen or if 24 hours have elapsed.
#

import sys
import datetime
import socket
import platform
import re
import uuid
import requests
import json
import time
import os.path

from dateutil.tz import tzlocal 

# set up some variables
heartbeat=0
firstrun=0
newip=0
delta=0

# parse time and timezone
runtime = datetime.datetime.now()
runtimef = runtime.strftime("%Y-%m-%d %H:%M:%S")
runtimez = datetime.datetime.now(tzlocal()).tzname()
runtimee = int(time.time())

# get local hostname and local IP address and local MAC
#localhostname = socket.gethostname()
localhostname = platform.node()
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

# return ipinfo content to variables
publicip=ipinfodata["ip"]

if 'ip' in ipinfodata:
   ip_loc=ipinfodata["loc"]
else:
   ip_loc="Not Returned"

if 'hostname' in ipinfodata:
   ip_hostname=ipinfodata["hostname"]
else:
   ip_hostname="Not Returned"

if 'org' in ipinfodata:
   ip_org=ipinfodata["org"]
else:
   ip_org="Not Returned"

if 'postal' in ipinfodata:
   ip_postal=ipinfodata["postal"]
else:
   ip_postal="Not Returned"

if 'city' in ipinfodata:
   ip_city=ipinfodata["city"]
else:
   ip_city="Not Returned"

if 'country' in ipinfodata:
   ip_country=ipinfodata["country"]
else:
   ip_country="Not Returned"

# what time is it right now and what publicip did we have?
iptime = ("%s:%s" % (runtimee,publicip)) 

#local temp file
ipfile = "/tmp/getendpointinfo.tmp"

# logic to check when we ran last and also figure out how long ago that was
if os.path.isfile(ipfile):
   firstrun=0
   with open(ipfile) as fp:
       line = fp.readline()
       oldtime,oldip=line.split(":") 
       delta=int(runtimee)-int(oldtime)
       if delta>86400:
          heartbeat=1
       else:
          heartbeat=0
       if publicip==oldip: 
          newip=0
       else:
          newip=1
else:
   #no file seen, assume never run before
   firstrun=1

def outputandwrite():
     print ("%s host_tz=\"%s\" hostname=\"%s\" local_ip=\"%s\" public_ip=\"%s\" local_mac=\"%s\" ip_location=\"%s\" ip_city=\"%s\" ip_country=\"%s\" ip_hostname=\"%s\" ip_org=\"%s\" ip_postal=\"%s\"" % (runtimef,runtimez,localhostname,localip,publicip,localmac,ip_loc,ip_city,ip_country,ip_hostname,ip_org,ip_postal))
     # write a file with the current IP
     ipfileo = open(ipfile,"w")
     ipfileo.write(iptime)
     ipfileo.close()

if (firstrun==1 and newip==0 and heartbeat==0):
     outputandwrite()
     sys.exit(0)

if (heartbeat==1 and newip==0):
     outputandwrite()
     sys.exit(0)

if (newip==1):
     outputandwrite()
     sys.exit(0)

#exit silently if no reportable condition
sys.exit(0)
