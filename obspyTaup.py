#!/usr/bin/python

from obspy.taup.taup import getTravelTimes
tt = getTravelTimes(delta=52.474, depth=611.0, model='ak135')
lentt=len(tt)
  
for i in range(0,lentt): 
   print(tt[i])
#   print(tt[i]['time'])
