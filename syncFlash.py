__author__ = 'bruno'


from obspy.core import read, UTCDateTime
from os import walk, sep, remove, path, makedirs, system, getcwd as pwd
from optparse import OptionParser

## Usage string:
use = "Usage: %syncFlash --flash [FLASH_PATH/CHANNEL] --sds [SDS_PATH/CHANNEL]"
desc = """Script to move data from FlashCard -> SDS. Remember to do ONE channel per time!!!"""
## Calling Parser:
parser = OptionParser(usage = use, description = desc)
## Options:
parser.add_option("-f", "--flash",   dest="flash", type = str, help="FLASH PATH containing Data collected")
parser.add_option("-s", "--sds",   dest="sds",    type = str, help="SDS PATH containing Archive Data")
## Parsing options into variables:
opts, args = parser.parse_args()
### Making sure all mandatory options appeared:
mandatory = ["flash", "sds"]
for m in mandatory:
    if not opts.__dict__[m]:
        print "\nmandatory option is missing\n"
        parser.print_help()
        exit(-1)


# Filling vars
#sds =       "/Users/bruno/Desktop/SDS/2013/BL/ITAB/HHE.D/"
#flashPath = "/Users/bruno/Desktop/2013/BL/ITAB/HHE.D/"
sds = opts.sds
flashPath = opts.flash
allFiles = []

## O comando rsync tarablha de maneiras diferentes de o path eh passado sem a 'barra' final (eg. path/).
## Por isso eh preciso fazer essa verificacao e garantir que a barra esteja lah.
if sds[-1:] != '/' :
    print 'Your SDS path does not have a final / but we added one for you.'
    sds = sds + '/'
    print sds

if flashPath[-1:] != '/' :
    print 'Your cFlash path does not have a final / but we added one for you.'
    flashPath = flashPath + '/'
    print flashPath

## To begin, we need to know the 1st and the last file in the flash path
## cuz we will merge them (they may not have all samples) and after, remove them from path
## For the others, we will use rsync to update the SDS.
for root, dirs, files in walk(flashPath):
    files.sort()
    for file in files :
        allFiles.append(file)
 
## Setting Files:
firstFile = allFiles[0]
lastFile = allFiles[len(allFiles)-1]
 
## Verify if first file exists in SDS and try to merge them
## If merged, remove file from flash path
if path.isfile(sds+firstFile) :
    st =  read(flashPath+firstFile)
    st += read(sds+firstFile)
    st.merge(method=-1)
    st.sort(['starttime'])
    print "joiningfirst file... %s %s" % (flashPath+firstFile, sds+firstFile)
    st.write(sds+firstFile, "MSEED")
    remove(flashPath+firstFile)
 
## Verify if last file exists in SDS and try to merge them
## If merged, remove file from flash path
if path.isfile(sds+lastFile) :
    st =  read(flashPath+lastFile)
    st += read(sds+lastFile)
    st.merge(method=-1)
    st.sort(['starttime'])
    print "joining last file... %s %s" % (flashPath+lastFile, sds+lastFile)
    st.write(sds+lastFile, "MSEED")
    remove(flashPath+lastFile)
 
## Now, this border problem is solved.
## Let's move to rsync part...
system('rsync -rv --remove-source-files %s %s' % (flashPath, sds))









