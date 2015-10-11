#!/usr/bin/python

import datetime
from obspy.core import UTCDateTime

year=int(datetime.datetime.strftime(datetime.datetime.now(), '%Y'))
month=int(datetime.datetime.strftime(datetime.datetime.now(), '%m'))
day=int(datetime.datetime.strftime(datetime.datetime.now(), '%d'))
hour=int(datetime.datetime.strftime(datetime.datetime.now(), '%H'))
minute=int(datetime.datetime.strftime(datetime.datetime.now(), '%M'))
second=int(datetime.datetime.strftime(datetime.datetime.now(), '%S'))

#print year
#print month
#print day
#print hour
#print minute
#print second

a=UTCDateTime(year, month, day, hour, minute, second)
b=a-600

print a
print b
