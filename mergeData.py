#!/usr/bin/python

from optparse import OptionParser
from obspy.core import read

use = "Usage: mergeData.py -a File1 -b File2 -o Fileout"
desc = """Script to merge two mseed file V1.0 25/01/2016 - M. Rocha                     

This Script can be used when is necessary merge data resulting of a stop in the Station
                                                                            
ex:                                                                                
get-evlist.py -b 2014-001 -e 2014-010 -l 1 -m 9 -s 1                                                        
"""
# Calling Parser:
parser = OptionParser(usage = use, description = desc)

parser.add_option("-a", "--file1", dest="fa", type = str, help="File 1")
parser.add_option("-b", "--file2", dest="fb", type = str, help="File 2")
parser.add_option("-o", "--fileout", dest="fo", type = str, help="File Out")

opts, args = parser.parse_args()

mandatories = ["fa", "fb", "fo"]
for m in mandatories:
    if not opts.__dict__[m]:
        print "\nmandatory option is missing\n"
        parser.print_help()
        exit(-1)


f1 = opts.fa
f2 = opts.fb
fout = opts.fo

st = read(f1)
st += read(f2)

st1 = read(f1)
st2 = read(f2)


#st1.plot()
#st2.plot()

#st.sort(['starttime'])

st.merge(method=1, fill_value="interpolate", interpolation_samples=-1)
#st.merge(method=1, fill_value="latest", interpolation_samples=-1)
#st.merge(method=1, fill_value="interpolate")

for trace in st:
      trace.write(fout, format="MSEED")

ffoo = read(fout)
ffoo.plot()
