__author__ = 'bruno'

from obspy.core import read, UTCDateTime
from os import walk, sep, remove, path, makedirs
from shutil import move
import smtplib
import logging


now = str(UTCDateTime.now())[:19].replace(':','-')
 
## Filling vars
sds = "/SDS"
sdsNRT = "/SDS-NRT"
logFile = '/home/suporte/nrtSync_logs/nrtSync.'+now+'.log'
 
logging.basicConfig(filename=logFile,level=logging.DEBUG)
 
nJoinedFiles = 0
nMovedFiles  = 0
jdays = []
 
 
## Control Vars
noErrors = True
 
 
for root, dirs, files in walk(sdsNRT): ## walking NRT path
    for nrtFile in files:
        try:
            st = read(root+sep+nrtFile) ## read a NRT file and get info from header
            print nrtFile, "read."
            logging.info(nrtFile + " read.")
   
            ## 1st Check: if the station found @ header is the same @ fileName        
            for tr in st:
                sta = tr.stats.station
                staError = False
                if sta not in nrtFile :
                    errorMessage = "1st check failed. Station code: " + sta + " is different than in fileName: " + nrtFile
                    print errorMessage
                    logging.error(errorMessage)
                    staError = True
                    noErrors = False
                     
            if not staError :
                message = "1st check passed"
                print message
                logging.info(message)
                jday = st[0].stats.starttime.julday
                if jday not in jdays :
                    jdays.append(jday)
            ## End of 1st check!
 
            ## 2nd Check???
            ## End of 2nd check!
 
            ## 3rd Check???
            ## End of 2rd check!             
             
            ## All OK? Then, sync.
            if noErrors :
                message = "All checks passed, synchronizing " + nrtFile
                print message
                logging.info(message) 
                 
                    
                year = str(st[0].stats.starttime.year)
                net  = st[0].stats.network
                sta  = st[0].stats.station
                cha  = st[0].stats.channel
                jday = st[0].stats.starttime.julday
                if jday not in jdays :
                    jdays.append(jday)
 
                sdsPath = sds+"/"+year+"/"+net+"/"+sta+"/"+cha+".D/"   
 
                if path.isfile(sdsPath+nrtFile): ## check if nrtFile exists in SDS, if true, merge them.
                    print nrtFile, "exists in SDS, I will try to merge."
                    logging.info(nrtFile + " exists in SDS, I will try to merge.")
                    st += read(sdsPath+nrtFile)
                    # 2014-07-03 # st.merge(method=1, interpolation_samples=0, fill_value="interpolate")
                    st.merge(method=-1)
                    st.sort(['starttime'])
                    st.write(sdsPath+nrtFile, "MSEED")
                    print nrtFile, "joined."
                    logging.info(nrtFile + " joined.")
                    remove(root+sep+nrtFile)
                    nJoinedFiles += 1
 
                else: ## check if station exists in SDS, if yes, move files, if not, create dirs and move files
                    if not path.isdir(sdsPath):
                    ## Now we have to check if this data comes from a station that is new to the system,
                    ## e.g, a station that was recently deployed and is sending its very 1st data.
                    ## In this case, we need to build the SC3 structure manually, cuz we are
                    ## synching files, not folders here. So, these next vars will help to do this job.
                        try:
                            makedirs(sdsPath)
                        except:
                            pass
                    move(root+sep+nrtFile, sdsPath)
                    print nrtFile, "not in SDS, moved."
                    logging.info(nrtFile + " not in SDS, moved.")
                    nMovedFiles += 1
                     
                     
        except Exception as e:
            logging.exception("Something is wrong, look: " + str(e))
 
jdays.sort()



server = smtplib.SMTP('smtp.gmail.com', 587)
 
sender = 'obsistec@gmail.com'
receivers = ['bruno@iag.usp.br', 'marcelorocha@unb.br']
#receivers = ['bruno@iag.usp.br']
  
text = "\n### nrtSync Bulletin ###\nnumber of Joined files: " + str(nJoinedFiles) + \
          "\nnumber of moved files: " + str(nMovedFiles) + \
          "\ndays affected: " + str(jdays) + "\n"

subject =  'nrtSync Bulletin'

message = 'Subject: %s\n\n%s' % (subject, text)

print message
logging.info(message)
 
#Next, log in to the server and send the email
server.starttls()
server.login("obsistec@gmail.com", "sisobsistecunb")
server.sendmail(sender, receivers, message)


