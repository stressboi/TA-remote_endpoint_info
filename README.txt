A simple Python script that leverages ipinfo.io to grab host details.

The idea here is to use this to track "remote" endpoints running the 
Splunk UF in modern, cloud environments with a mobile workforce. The
script is provided in .py (should run fine with no dependencies on a 
Linux or Mac host) and also in a Windows executable.

For Windows, set the executable to be owned by the SYSTEM user so that
the UF may run it.

