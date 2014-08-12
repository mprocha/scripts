#!/usr/bin/python

from obspy.iris import Client
#from obspy.fdsn import Client
client = Client()
result = client.distaz(stalat=1.1, stalon=1.2, evtlat=3.2, evtlon=1.4)
print(result['distance'])
print(result['backazimuth'])
print(result['azimuth'])

