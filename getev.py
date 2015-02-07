#!/usr/bin/python

from obspy.core import read, UTCDateTime
from obspy.arclink import Client
import obspy.iris.client as iclient 
from obspy.taup.taup import getTravelTimes
from obspy.sac import SacIO
from optparse import OptionParser
from os import mkdir

# teste
# Usage string:
use = "Usage: %prog -n NET -s STATION -c CHA (Default, ALL) -b YYYY-JDAY-HH-MM-SS.MSEC --elat=ELAT --elon=ELON --edep=EDEP -a SERVER "
desc = """Script criado para baixar arquivos de eventos do Servidor ArcLink                                                                                                                                                                          
Examples:                                                                                                                       
getev.py -n BR -s ARAG  -b 2014-108-14-27-22.883 --elat=17.146 --elon=-100.996 --edep=10.0 -a 1 """

# Calling Parser:
parser = OptionParser(usage = use, description = desc)

# Prog options:

parser.add_option("-n","--network", dest="net", type = str, help="network code")
parser.add_option("-s","--station", dest="sta", type = str, help="station code")
parser.add_option("-c","--channel", dest="cha", type = str, help="channel code", default="*")
parser.add_option("-b","--btime", dest="b", type = str, help="e.g YYYY-JUL-HH-MM-SS, Event to download")
parser.add_option("--elat", dest="elat", type = str, help="Event Latitude")
parser.add_option("--elon", dest="elon", type = str, help="Event Laingitude")
parser.add_option("--edep", dest="edep", type = float, help="Event Depth")
#parser.add_option("-o", "--outFile", dest="out", type = str, help="outfile types: 1=SAC 2=MSEED")
parser.add_option("-a", "--serv", dest="serv", type = str, help="Arclink Server: 1=UnB 2=IAG 3=ON 4=IRIS")


# The final step is to parse the options and arguments into variables we can use later:
opts, args = parser.parse_args()


# Making sure all mandatory options appeared:
mandatories = ["net", "sta", "b"]
for m in mandatories:
    if not opts.__dict__[m]:
        print "\nmandatory option is missing\n"
        parser.print_help()
        exit(-1)


## Checking Out File Option:
#outTypes = ["1", "2"]
#if opts.out not in outTypes:
#        print "\noutfile type is not allowed\n"
#        parser.print_help()
#        exit(-1)

#out = opts.out
#if out == "1" :
#    _format = "SAC"
#    ext = ".sac"
#else :
#    _format = "MSEED"
#    ext = ".mseed"

# Checking Server Option:
servTypes = ["1", "2", "3", "4"]
if opts.serv not in servTypes:
        print "\nServer type is not allowed\n"
        parser.print_help()
        exit(-1)

serv = opts.serv
if serv == "1" :
	### Cliente UnB:
	client = Client(host="datasisInt.unb.br", port=18001, user="marcelorocha@unb.br")
        #client = Client(host="164.41.28.154", port=18001)
elif serv == "2":
	### Cliente USP:
	client = Client(host="seisrequest.iag.usp.br", port=18001, user="marcelorocha@unb.br")
	#client = Client(host="seisrequest.iag.usp.br", port=18001)
elif serv == "3":
	### Cliente ON:
	client = Client(host="rsis1.on.br", port=18001, user="marcelorocha@unb.br")
	#client = Client(host="rsis1.on.br", port=18001)
elif serv == "4":
	### Cliente IRIS:
	client = Client(host="rtserve.iris.washington.edu", port=18001, user="marcelorocha@unb.br")



# Setting up Vars...
net = opts.net
sta = opts.sta
cha = opts.cha
b = UTCDateTime(opts.b)
elat = opts.elat
elon = opts.elon 
edep = opts.edep
year=b.year
jul=b.julday
hour=b.hour
min=b.minute
sec=b.second

#Getting Station Latitude and Longitude:
stadic = client.getInventory(net,station=sta)
slat = stadic.get(net+"."+sta).get("latitude")
slon = stadic.get(net+"."+sta).get("longitude")
selv = stadic.get(net+"."+sta).get("elevation")
#print slat
#print slon

# Calculate gcarc, baz and az:
irisclient = iclient.Client()
gcbazaz = irisclient.distaz(stalat=slat, stalon=slon, evtlat=elat, evtlon=elon) 
gcarc = gcbazaz.get('distance')
baz = gcbazaz.get('backazimuth')
az = gcbazaz.get('azimuth')
#print gcarc
#print baz
#print az

# Calculate Travel Time:
ttlist = getTravelTimes(delta=gcarc, depth=edep ,model='iasp91')
for num in range(len(ttlist)):
    ttdic=ttlist[num]
    phase=ttdic.get('phase_name')
    if phase == 'P':
         ptoa=ttdic.get('take-off angle')
         ptime=ttdic.get('time')
    elif phase == 'S':
         stoa=ttdic.get('take-off angle')
         stime=ttdic.get('time')
#         print toa
#         print ptime

# Fix date format:
syear=str(year)

if jul < 10:
	sjul="00"+str(jul)
elif jul < 100:
	sjul="0"+str(jul)
else:
	sjul=str(jul)

if hour < 10:
	shour="0"+str(hour)
else:
	shour=str(hour)

if min < 10:
	smin="0"+str(min)
else:
	smin=str(min)

if sec < 10:
	ssec="0"+str(sec)
else:
	ssec=str(sec)

#dir="GETEVDIR"
dir=syear+"."+sjul+"."+shour+"."+smin+"."+ssec
print dir


try:
    print "trying to download day", "%03d" % jul, "..."
    st = client.getWaveform(net, sta, '*', cha, b ,  b + 8000)
    st.merge(method=1, fill_value="interpolate")
    try:
        mkdir(dir)
    except:
        pass
    for tr in st :
        loc = str(tr.stats.location)
        chan = str(tr.stats.channel)
        #date = str(tr.stats.starttime).replace("-", ".")
        year = str(tr.stats.starttime.year)
        jday = str("%03d" % tr.stats.starttime.julday)
#        filename = net+"."+sta+"."+loc+"."+chan+".D."+year+"."+jday+ext
        filename = syear+"."+sjul+"."+shour+"."+smin+"."+ssec+"."+sta+"."+chan+".sac"
        tr.write(dir+"/"+filename, format="SAC")
        t=SacIO()
        t.SetHvalueInFile(dir+"/"+filename,'a',ptime)
        t.SetHvalueInFile(dir+"/"+filename,'ka','P')
        t.SetHvalueInFile(dir+"/"+filename,'t0',stime)
        t.SetHvalueInFile(dir+"/"+filename,'kt0','S')
        t.SetHvalueInFile(dir+"/"+filename,'stla',slat)
        t.SetHvalueInFile(dir+"/"+filename,'stlo',slon)
        t.SetHvalueInFile(dir+"/"+filename,'stel',selv)
        t.SetHvalueInFile(dir+"/"+filename,'knetwk',net)
        t.SetHvalueInFile(dir+"/"+filename,'evla',elat)
        t.SetHvalueInFile(dir+"/"+filename,'evlo',elon)
        t.SetHvalueInFile(dir+"/"+filename,'evdp',edep)
        t.SetHvalueInFile(dir+"/"+filename,'az',az)
        t.SetHvalueInFile(dir+"/"+filename,'baz',baz)
        t.SetHvalueInFile(dir+"/"+filename,'gcarc',gcarc)
        print filename, "saved."
except:
    print "... no data found."
    pass
jul += 1
b = b + 24*3600

 
print "\nno more data to retrieve.\n"
