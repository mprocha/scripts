#!/usr/bin/python

from obspy import read
from optparse import OptionParser

## Usage string:
use = "Usage: segy2sac.py -f file"
desc = """Script to convert a SEGY-file to SAC-format"""

## Calling Parser:
parser = OptionParser(usage = use, description = desc)
## Options:
parser.add_option("-f", "--file",   dest="file", type = str, help="SEGY-file path")
## Parsing options into variables:
opts, args = parser.parse_args()
### Making sure all mandatory options appeared:
mandatory = ["file"]
for m in mandatory:
    if not opts.__dict__[m]:
        print ""
        parser.print_help()
        print ""
        print "Ex: "
        print "segy2sac.py -f ./file.segy"
        print ""
        print "Marcelo Rocha - UnB - 2014/04/21 - V1.0"
        print ""
        exit(-1)

filer=opts.file

st=read(filer)
st.write("test.sac",format="SAC")
print ""
print "A SAC-file (test.sac) was created in your workdir"
print "" 
quit()

