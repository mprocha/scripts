#!/usr/bin/python

from obspy.core import read, UTCDateTime
from obspy.arclink import Client
from obspy.sac import SacIO
from optparse import OptionParser
from os import mkdir


# dumb message...
print "\nBulk Data Downloader - IAG-USP - 2012\n"


# Usage string:
use = "Usage: %prog -n NET -s STATION -c CHA (Default, ALL) -b YYYY-DAY -e YYYY-DAY"
desc = """Script criado para baixar arquivos de 24h do Servidor ArcLink IAG-USP"""

# Calling Parser:
parser = OptionParser(usage = use, description = desc)

# Prog options:

parser.add_option("-n", "--network", dest="net", type = str, help="network code")
parser.add_option("-s", "--station", dest="sta", type = str, help="station code")
parser.add_option("-c", "--channel", dest="cha", type = str, help="channel code", default="*")
parser.add_option("-b", "--btime", dest="b", type = str, help="e.g YYYY-JULDAY, First Day to download")
parser.add_option("-e", "--etime", dest="e", type = str, help="e.g YYYY-JULDAY, Last Day to download")
parser.add_option("-o", "--outFile", dest="out", type = str, help="outfile types: 1=SAC 2=MSEED")

# The final step is to parse the options and arguments into variables we can use later:
opts, args = parser.parse_args()


# Making sure all mandatory options appeared:
mandatories = ["net", "sta", "b", "e"]
for m in mandatories:
    if not opts.__dict__[m]:
        print "\nmandatory option is missing\n"
        print ""
        parser.print_help()
        print ""
        print "Ex: "
        print "get24h.py -n BR -s IPMB -b 2013-350 -e 2013-355 -o 2"
        print ""
        print "Marcelo Rocha - UnB - 2014/04/21 - V1.0"
        print ""
        exit(-1)


# Checking Out File Option:
outTypes = ["1", "2"]
if opts.out not in outTypes:
        print "\noutfile type is not allowed\n"
        print ""
        parser.print_help()
        print ""
        print "Ex: "
        print "get24h.py -n BR -s IPMB -b 2013-350 -e 2013-355 -o 2"
        print ""
        print "Marcelo Rocha - UnB - 2014/04/21 - V1.0"
        print ""
        exit(-1)


out = opts.out
if out == "1" :
    _format = "SAC"
else :
    _format = "MSEED"

# Setting up Vars...
net = opts.net
sta = opts.sta
cha = opts.cha
b = UTCDateTime(opts.b) + 5
e = UTCDateTime(opts.e)
jday1 = int(opts.b[-3:])
jday2 = int(opts.e[-3:])


print jday2 - jday1, "day(s) to search for.\n"


# Retrieve waveforms via ArcLink
#client = Client(host="seisrequest.iag.usp.br", port=18001)
client = Client(host="seisrequest.iag.usp.br", port=18001)
#client = Client(host="rsis1.on.br", port=18001)

# Teste para baiar dados do IRIS:
#client = Client(host="rtserve.iris.washington.edu", port=18001)

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
