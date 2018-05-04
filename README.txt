A simple Python script that leverages ipinfo.io to grab host details.

The idea here is to use this to track "remote" endpoints running the 
Splunk UF in modern, cloud environments with a mobile workforce. The
script is provided in .py (should run fine with no dependencies on a 
Linux or Mac endpoint) and also in a Windows executable tested on 
64 bit Windows 7 and Windows 10.

Run it every hour or more frequently. However, one might consider
blocking traffic to ipinfo.io from behind corporate firewall from endpoint
IP ranges, because it is likely that ipinfo.io will shut you down due to
excessive requests.

However, IRL this will not be an issue since endpoints will be coming
from varied address space (assuming this is used for the intended purpose
of tracking IP addresses of remote users.) An intermediate forwarder
in a DMZ is a critical aspect of this design, so that endpoints can 
communicate to a Splunk instance regardless of what public network
they are on.

For Windows, set the executable to be owned by the SYSTEM user so that
the UF may run it.

Sample output when it works looks like this, which Splunk automatically
parses due to KV pair format:

2018-05-03 23:51:20 hosttz="Mountain Daylight Time" hostname="fishingderby" local_ip="192.168.10.205" public_ip="23.92.XXX.10" localmac="bc:5f:f4:e6:49:2b" ip_location="53.2851,-6.3713" ip_country="IE" ip_city="Dublin" ip_hostname="10.XXX.92.23.static.wiifi.net" ip_org="AS47536 Global IP Exchange" ip_postal="d24"

brodsky@splunk.com
5-3-2018
