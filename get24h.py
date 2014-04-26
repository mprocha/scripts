#!/usr/bin/python

from obspy.core import read, UTCDateTime
from obspy.arclink import Client
from obspy.sac import SacIO
from optparse import OptionParser
from os import mkdir


# dumb message...
print "\nBulk Data Downloader - UnB - 2014"
print "Modified from Bulk Data Download - IAG-USP - 2012"


# Usage string:
use = "Usage: %prog -n NET -s STATION -c CHA (Default, ALL) -b YYYY-DAY -e YYYY-DAY"
desc = """Script criado para baixar arquivos de 24h do Servidor ArcLink"""

# Calling Parser:
parser = OptionParser(usage = use, description = desc)

# Prog options:

parser.add_option("-n", "--network", dest="net", type = str, help="Network code")
parser.add_option("-s", "--station", dest="sta", type = str, help="Station code")
parser.add_option("-c", "--channel", dest="cha", type = str, help="Channel code", default="*")
parser.add_option("-b", "--btime", dest="b", type = str, help="e.g YYYY-JULDAY, First Day to download")
parser.add_option("-e", "--etime", dest="e", type = str, help="e.g YYYY-JULDAY, Last Day to download")
parser.add_option("-o", "--outFile", dest="out", type = str, help="Outfile types: 1=SAC 2=MSEED")
parser.add_option("-a", "--arclink", dest="arc", type = str, help="Arclink Server types: 1=UnB 2=IAG 3=IRIS 4=ON")

# The final step is to parse the options and arguments into variables we can use later:
opts, args = parser.parse_args()


# Making sure all mandatory options appeared:
mandatories = ["net", "sta", "b", "e"]
for m in mandatories:
    if not opts.__dict__[m]:
        print "\nMandatory option is missing: [ "+m+" ]\n"
        parser.print_help()
        print "Ex: \n"
        print "get24h.py -n BR -s IPMB -b 2013-350 -e 2013-355 -o 2 -a 3\n"
        print "Marcelo Rocha - UnB - 2014/04/26 - V2.0\n"
        exit(-1)


# Checking Out File Option:
outTypes = ["1", "2"]
if opts.out not in outTypes:
        print "\nOutfile type is not allowed\n"
        parser.print_help()
        print "Ex: \n"
        print "get24h.py -n BR -s IPMB -b 2013-350 -e 2013-355 -o 2 -a 3\n"
        print "Marcelo Rocha - UnB - 2014/04/26 - V2.0\n"
        exit(-1)


out = opts.out
if out == "1" :
    _format = "SAC"
else :
    _format = "MSEED"


# Checking Arklink Server Option:
arcTypes = ["1", "2", "3", "4"]
if opts.arc not in arcTypes:
        print "\nArclink type is not allowed\n"
        parser.print_help()
        print "Ex: \n"
        print "get24h.py -n BR -s IPMB -b 2013-350 -e 2013-355 -o 2 -a 3\n"
        print "Marcelo Rocha - UnB - 2014/04/26 - V2.0\n"
        exit(-1)

#Retrieve waveforms via ArcLink
arc = opts.arc
if arc == "1" :
    client = Client(host="164.41.28.153", port=18001)
elif arc == "2":
    client = Client(host="seisrequest.iag.usp.br", port=18001)
elif arc == "3" :
    client = Client(host="rtserve.iris.washington.edu", port=18001)
elif arc == "4" :
    client = Client(host="rsis1.on.br", port=18001)

# Setting up Vars...
net = opts.net
sta = opts.sta
cha = opts.cha
b = UTCDateTime(opts.b) + 5
e = UTCDateTime(opts.e)
jday1 = int(opts.b[-3:])
jday2 = int(opts.e[-3:])


print jday2 - jday1, "day(s) to search for.\n"



while jday1 <= jday2 :
   
    try:
        print "trying to download day", "%03d" % jday1, "..."
        st = client.getWaveform(net, sta, '*', cha, b,  b + 86390)
        st.merge(method=1, fill_value="interpolate")
        try:
            mkdir(sta)
        except:
            pass
        for tr in st :
            loc = str(tr.stats.location)
            chan = str(tr.stats.channel)
            #date = str(tr.stats.starttime).replace("-", ".")
            year = str(tr.stats.starttime.year)
            jday = str("%03d" % tr.stats.starttime.julday)
            filename = net+"."+sta+"."+loc+"."+chan+".D."+year+"."+jday
            tr.write(sta+"/"+filename, format=_format)
            print filename, "saved."
    except:
        print "... no data found."
        pass
    jday1 += 1
    b = b + 24*3600
   
print "\nno more data to retrieve.\n"
