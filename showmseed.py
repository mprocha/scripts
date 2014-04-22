#!/usr/bin/python

from obspy.core import read
from optparse import OptionParser

## Usage string:
use = "Usage: showmseed.py -f file"
desc = """Script to print a mseed data"""

## Calling Parser:
parser = OptionParser(usage = use, description = desc)
## Options:
parser.add_option("-f", "--file",   dest="file", type = str, help="MSEED FILE PATH containing Data collected")
## Parsing options into variables:
opts, args = parser.parse_args()
### Making sure all mandatory options appeared:
mandatory = ["file"]
for m in mandatory:
    if not opts.__dict__[m]:
        print("")
        parser.print_help()
        print(" ")
        print("Ex: ")
        print("showmseed.py -f /SDS/2014/BR/ARAG/HHZ.D/BR.ARAG..HHZ.D.2014.110")
        print("")
        print("Marcelo Rocha - UnB - 2014/04/21 - V1.0")
        print("")
        exit(-1)

filer=opts.file

print(filer)

singlechannel=read(filer)
#singlechannel.plot()
singlechannel.plot(type='dayplot')

