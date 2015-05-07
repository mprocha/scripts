#!/usr/bin/python

from obspy import read
st=read('AI-BELA-2014.miniseed')
st.write("test.sac",format="SAC")
quit()

