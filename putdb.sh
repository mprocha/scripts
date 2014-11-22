#!/bin/bash

usage(){
if [ -z $1 ]
then 
   echo "usage: putdb.sh <database-name> "
   echo " "
   echo "application: external_sc3"
   echo "processing: seiscomp3"
   echo " "
fi
}

base=$1

if [ $base == seiscomp3 ]
then 
   for ev in *.xml
   do
      scdb -i $ev -d mysql://sysop:sysop@164.41.28.154/seiscomp3 -b 1000
   done
elif [ $base == external_sc3 ]
then
   for ev in *.xml
   do
      scdb -i $ev -d mysql://sysop:sysop@164.41.28.153/external_sc3 -b 1000
   done
else
  usage   
  exit
fi

