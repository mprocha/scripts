#!/usr/bin/python

from obspy import read
st=read('BR.RET2..HHZ.D.2009.338')
st.write("test.sac",format="SAC")
quit()

