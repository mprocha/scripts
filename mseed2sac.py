#!/usr/bin/python

from obspy import read
import os, sys

path="/home/marcelo/tmp"
a=os.listdir( path )

for item in a:

  #st=read('AI-BELA-2014.miniseed')
  print item
  st=read(path+"/"+item)
  st.write("/home/marcelo/"+item+".sac",format="SAC")

quit()

