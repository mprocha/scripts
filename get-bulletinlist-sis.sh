#!/bin/bash

# Script to generate a event list from Obsis Seiscomp Databases:
# Marcelo Rocha - UnB - 2014/11/14 - V1.0

usage(){
   echo " "
   echo "Script to generate a event list from Obsis Seiscomp Database"
   echo " "
   echo "Marcelo Rocha - UnB - 14-11-2013 - V1.0"
   echo "email: marcelorocha.unb@gmail.com"
   echo " "
   echo "Usage:"
   echo "get-bulletinlist-sis.sh [bdate] [btime] [edate] [etime]"
   echo " "
   echo "flags:"
   echo "bdate <date to begin>  Option to choose the date to begin the eventlist YYYY-MM-DD"
   echo "btime <time to begin>  Option to choose the time to begin the eventlist HH:MM:SS"
   echo "edate <date to end>    Option to choose the date to end the eventlist YYYY-MM-DD"
   echo "etime <time to end>    Option to choose the time to end the eventlist HH:MM:SS"
   echo " "
   echo "Ex: "
   echo "get-bulletinlist-sis.sh 2014-11-10 00:00:00 2014-11-13 23:59:59"
   echo " "
}

bdate=$1
btime=$2
edate=$3
etime=$4

if [ -z $bdate ]
then
   usage
   exit 1
fi

if [ -z $btime ]
then
   usage
   exit 1
fi

if [ -z $edate ]
then
   usage
   exit 1
fi

if [ -z $etime ]
then
   usage
   exit 1
fi

begin=$bdate" "$btime
end=$edate" "$etime

#echo $begin
#echo $end

#> evtlist.txt
for evt in $(seiscomp exec scevtls -d mysql://sysop:sysop@164.41.28.154/seiscomp3 --begin "${begin}" --end "${end}"); do
        scbulletin -E $evt -3 -x -d mysql://sysop:sysop@164.41.28.154/seiscomp3 
        echo " "
        echo "#####################################################################"
        echo " "
done


