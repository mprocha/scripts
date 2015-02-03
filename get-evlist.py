#!/usr/bin/python

from obspy.fdsn import Client as fdsnClient
from obspy.core import UTCDateTime
from obspy.core.event import readEvents
from optparse import OptionParser

#teste
# Usage string:
use = "Usage: get-evlist.py -b YYYY-JDAY -e YYYY-JDAY -l M -m M -s (1-IRIS; 2-IAG)"
desc = """Script to get a event list from a FDSN server - V2.0 30/03/2014 - M. Rocha                     

Script generate a file (evlist.txt) with the follow rows:                                            
                                                                                          
yyyy mm dd (jjj) hh min sec msec lat lon dep mag mag_type eval_mode status
                                                                            
ex:                                                                                
get-evlist.py -b 2014-001 -e 2014-010 -l 5 -m 9 -s 1

"""

# Calling Parser:
parser = OptionParser(usage = use, description = desc)

# Prog options:

parser.add_option("-b", "--beg", dest="tmin", type = str, help="Begin time")
parser.add_option("-e", "--end", dest="tmax", type = str, help="End time")
parser.add_option("-l", "--mmin", dest="mmin", type = str, help="Minimium Magnitude", default="0")
parser.add_option("-m", "--mmax", dest="mmax", type = str, help="Maximum Magnitude", default="9")
#parser.add_option("-s", "--serv", dest="serv", type = str, help="FDSN Server: 1=IRIS 2=IAG")
parser.add_option("-s", "--serv", dest="serv", type = str, help="FDSN Server: 1=UnB (Default) 2=IAG 3=IRIS")

# The final step is to parse the options and arguments into variables we can use later:
opts, args = parser.parse_args()

# Making sure all mandatory options appeared:
mandatories = ["tmin", "tmax", "mmin", "mmax", "serv"]
for m in mandatories:
    if not opts.__dict__[m]:
        print "\nmandatory option is missing\n"
        parser.print_help()
        exit(-1)


# Checking Out File Option:
servTypes = ["1", "2", "3"]
if opts.serv not in servTypes:
        print "\nServer FDSN type is not allowed\n"
        parser.print_help()
        exit(-1)

serv = opts.serv
if serv == "3" :
	fdsn=fdsnClient(base_url="IRIS")
elif serv == "2":
	fdsn=fdsnClient(base_url="http://moho.iag.usp.br")
else:
        fdsn=fdsnClient(base_url="http://164.41.28.154:8080")

# Setting up Vars...
tmin = UTCDateTime(opts.tmin)
tmax = UTCDateTime(opts.tmax)
mmin = opts.mmin
mmax = opts.mmax

#year=b.year
#jul=b.julday
#hour=b.hour
#min=b.minute
#sec=b.second


#iyear=str(2013)
#imm=str(11)
#idd=str(01)
#ihh=str(00)
#imi=str(00)
#ise=str(00)
#
#fyear=str(2013)
#fmm=str(12)
#fdd=str(01)
#fhh=str(00)
#fmi=str(00)
#fse=str(00)

#minmag=0.0
#maxmag=4.0

#tmin=UTCDateTime("2013-11-01 00:00:00")
#tmin=UTCDateTime(iyear+"-"+imm+"-"+idd+" "+ihh+":"+imi+":"+ise)
#print tmin

#tmax=UTCDateTime("2013-12-01 00:00:00")
#tmax=UTCDateTime(fyear+"-"+fmm+"-"+fdd+" "+fhh+":"+fmi+":"+fse)
#print tmax

catalog=fdsn.get_events(starttime=tmin,
			endtime=tmax, 
			includearrivals=True,
			minmagnitude=mmin,
			maxmagnitude=mmax)

#catalog=fdsn.get_events(starttime=t0, endtime=t1, includearrivals=True,
#			includepicks=True, format="catalog")

#print catalog.__str__(print_all=True)

#cat2=catalog.filter("magnitude <= minmag")
#print cat2.__str__(print_all=True)

f=open("evlist.txt","w")
for event in catalog:
	evpref=event.preferred_origin()
	magpref=event.preferred_magnitude()

#	print "####### Inicio #######"
#	print evpref
#	print magpref

### Time is in UTCDateTime format (elements not separated)
#	print "%s %7.3f %8.3f %9.3f %6.3f %s" % (evpref.time,evpref.latitude,evpref.longitude,evpref.depth/1000,
#					magpref.mag,magpref.magnitude_type)

	year=evpref.time.year
	mm=evpref.time.month
	dd=evpref.time.day
	jday=evpref.time.julday 
	hh=evpref.time.hour
	mn=evpref.time.minute
	sec=evpref.time.second
	micsec=evpref.time.microsecond
        msec=micsec/1000

	smicsec=str(micsec)

	syear=str(year)

	if mm < 10:
       		smm="0"+str(mm)
	else:
        	smm=str(mm)

	if dd < 10:
	        sdd="0"+str(dd)
	else:
	        sdd=str(dd)

	if jday < 10:
	        sjday="00"+str(jday)
	elif jday < 100:
	        sjday="0"+str(jday)
	else:
	        sjday=str(jday)

	if hh < 10:
	        shh="0"+str(hh)
	else:
	        shh=str(hh)

	if mn < 10:
	        smn="0"+str(mn)
	else:
	        smn=str(mn)

	if sec < 10:
	        ssec="0"+str(sec)
	else:
	        ssec=str(sec)

	if msec < 10:
	        smsec="00"+str(msec)
	elif msec < 100:
	        smsec="0"+str(msec)
	else:
	        smsec=str(msec)

#	print "%4d %2d %2d (%3d) %2d %2d %2d %6d %7.3f %8.3f %9.3f %6.3f %4s %9s %11s" % (	evpref.time.year,
#												evpref.time.month,
#												evpref.time.day,
#												evpref.time.julday, 
#												evpref.time.hour,
#												evpref.time.minute,
#												evpref.time.second,
#												evpref.time.microsecond/1000,
#												evpref.latitude,
#												evpref.longitude,
#												evpref.depth/1000,
#												magpref.mag,
#												magpref.magnitude_type,
#												evpref.evaluation_mode,
#												evpref.evaluation_status)

	f.write("%4s %2s %2s (%3s) %2s %2s %2s %3s %7.3f %8.3f %9.3f %6.3f %4s %9s %11s \n" % (	syear,
                                                                                		smm,
            	        	                                                            	sdd,
                	                                                                	sjday,
                               	               			                                shh,
                                	                                                	smn,
                                        	                                	        ssec,
                                                                                                smsec,
       		                                                                         	evpref.latitude,
                		                                                                evpref.longitude,
                                		                                                evpref.depth/1000,
                                                		                                magpref.mag,
                                                                		                magpref.magnitude_type,
												evpref.evaluation_mode,
												evpref.evaluation_status))

#
#for event in catalog.filter("standard_error < 0.5"):
#	evpref=event.preferred_origin()
#	magpref=event.preferred_magnitude()
#	if evpref.evaluation_mode=='manual':
#		print evpref 
##		print megpref

