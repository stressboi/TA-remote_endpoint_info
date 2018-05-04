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

2018-05-03 22:11:07 hosttz="Mountain Daylight Time" hostname="fishingderby" local_ip="10.10.1.205" public_ip="24.27.29.XXX" localmac="bc:5f:f4:e6:49:2b" ip_location="39.9355,-105.0470" ip_hostname="c-24-27-29-XXX.hsd1.co.comcast.net" ip_org="AS7922 Comcast Cable Communications, LLC" ip_postal="80020"

brodsky@splunk.com
5-3-2018
