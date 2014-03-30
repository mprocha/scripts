from obspy import read
st=read('395-01.sac')
st.write("teste.segy",format="SEGY")
quit()

