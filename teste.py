#!/usr/bin/python

from obspy.fdsn import Client
from obspy.core import UTCDateTime
from obspy.core.event import readEvents

fdsn=Client(base_url="http://datasisint.unb.br:8080")

tmin = UTCDateTime("2015-324")
tmax = UTCDateTime("2015-325")
mmin=1
mmax=9
rmin=3
rmax=10
lat=-11.6
lon=-56.7

#print str(tmin)+" "+str(tmax)+" "+str(mmin)+" "+str(mmax)+" "+str(rmin)+" "+str(rmax)+" "+str(lat)+" "+str(lon)

catalog=fdsn.get_events(starttime=tmin, endtime=tmax)

#, includearrivals=True, minmagnitude=str(mmin), maxmagnitude=str(mmax), latitude=str(lat), longitude=str(lon), minradius=str(rmin), maxradius=str(rmax))

for event in catalog:
        evpref=event.preferred_origin()
	author=evpref.creation_info.author
        #evid=evpref.resource_id
        evid=event.resource_id.id.replace("smi:scs/0.6/","")
        evtype=str(event.event_type).replace(" ","-")
	 

        print str(evid)+" "+author+" "+evtype
#print catalog

