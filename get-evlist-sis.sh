#!/bin/bash

# Script to generate a event list from Obsis Seiscomp Databases:
# Marcelo Rocha - UnB - 2014/11/13 - V1.0

usage(){
   echo " "
   echo "Script to generate a event list from Obsis Seiscomp Database"
   echo " "
   echo "Marcelo Rocha - UnB - 13-11-2013 - V1.0"
   echo "email: marcelorocha.unb@gmail.com"
   echo " "
   echo "Usage:"
   echo "get-evlist-sis.sh [bdate] [btime] [edate] [etime] [type]"
   echo " "
   echo "flags:"
   echo "bdate <date to begin>  Option to choose the date to begin the eventlist YYYY-MM-DD"
   echo "btime <time to begin>  Option to choose the time to begin the eventlist HH:MM:SS"
   echo "edate <date to end>    Option to choose the date to end the eventlist YYYY-MM-DD"
   echo "etime <time to end>    Option to choose the time to end the eventlist HH:MM:SS"
   echo "type  <type of event>  Option to choose the type of event:  automatic, manual, all (default)"
   echo " "
   echo "Ex: "
   echo "get-evlist-sis.sh 2014-11-10 00:00:00 2014-11-13 23:59:59  manual"
   echo " "
}

bdate=$1
btime=$2
edate=$3
etime=$4
mode=$5

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
#echo $mode

> evtlist.txt
for evt in $(seiscomp exec scevtls -d mysql://sysop:sysop@164.41.28.154/seiscomp3 --begin "${begin}" --end "${end}"); do
#        echo exporting $evt
        scbulletin -E $evt -3 -x -d mysql://sysop:sysop@164.41.28.154/seiscomp3 > tmp
        date=`cat tmp | grep Date | awk '{print $2}'`
        tempo=`cat tmp | grep Time | awk '{print $2}'`
        lat=`cat tmp | grep Latitude | awk '{print $2}'`
        lon=`cat tmp | grep Longitude | awk '{print $2}'`
        dep=`cat tmp | grep Depth | awk '{print $2}'`
        res=`cat tmp | grep Residual | awk '{print $3}'`
        if [ -z $res ]
        then
           res="No"
        fi
        azgap=`cat tmp | grep Azimuthal | awk '{print $3}'`
        if [ -z $azgap ]
        then
           azgap="No"
        fi
#        magMwp=`cat tmp | grep " Mwp " | awk '{print $2}'`        
#        magMwMwp=`cat tmp | grep " Mw(Mwp) " | awk '{print $2}'`        
#        magmB=`cat tmp | grep " mB " | awk '{print $2}'`        
#        magMwmB=`cat tmp | grep " Mw(mB) " | awk '{print $2}'`        
#        magM=`cat tmp | grep " M " | awk '{print $2}'`        
#        magmb=`cat tmp | grep " mb " | awk '{print $2}'`        
#        magMLv=`cat tmp | grep " MLv " | awk '{print $2}'`        
        magPrefValue=`cat tmp | grep " preferred " | awk '{print $2}'`
        magPrefTipo=`cat tmp | grep " preferred " | awk '{print $1}'`
        if [ -z $magPrefValue ]
        then
           magPrefValue="No"
           magPrefTipo="No"
        fi
        mod=`cat tmp | grep " Mode " | awk '{print $2}'`
        id=`cat tmp | grep " Public ID " | grep "unb" | awk '{print $3}'`        
        agency=`cat tmp | grep " Agency " | awk '{print $2}'`        
        reg=`cat tmp | grep "region name" | sed 's/      region name\://' | sed 's/      earthquake name\://' | sed 's/ //' | sed 's/ /\_/g'`
#        echo $date $tempo $lat $lon $dep $res $azgap $magMwp $magMwMwp $magmB $magMwmB $magM $magmb $magMLv $id $agency $reg 
#        echo $date $tempo $lat $lon $dep $res $azgap $magMwp $magMwMwp $magmB $magMwmB $magM $magmb $magMLv $id $agency $reg >> evtlist.txt
        if [ -z $mode ]
        then
           echo $date $tempo $lat $lon $dep $res $azgap $magPrefValue $magPrefTipo $mod $id $agency $reg \
| awk '{printf "%s %s %6s %6s %4s %7s %4s %5s %7s %9s %11s %3s %s\n", $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13}' 
           echo $date $tempo $lat $lon $dep $res $azgap $magPrefValue $magPrefTipo $mod $id $agency $reg \
| awk '{printf "%s %s %6s %6s %4s %7s %4s %5s %7s %9s %11s %3s %s\n", $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13}' >> evtlist.txt 
        elif [ $mode == all ]
        then
           echo $date $tempo $lat $lon $dep $res $azgap $magPrefValue $magPrefTipo $mod $id $agency $reg \
| awk '{printf "%s %s %6s %6s %4s %7s %4s %5s %7s %9s %11s %3s %s\n", $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13}' 
           echo $date $tempo $lat $lon $dep $res $azgap $magPrefValue $magPrefTipo $mod $id $agency $reg \
| awk '{printf "%s %s %6s %6s %4s %7s %4s %5s %7s %9s %11s %3s %s\n", $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13}' >> evtlist.txt 
        elif [ $mode == $mod ]
        then
           echo $date $tempo $lat $lon $dep $res $azgap $magPrefValue $magPrefTipo $mod $id $agency $reg \
| awk '{printf "%s %s %6s %6s %4s %7s %4s %5s %7s %9s %11s %3s %s\n", $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13}' 
           echo $date $tempo $lat $lon $dep $res $azgap $magPrefValue $magPrefTipo $mod $id $agency $reg \
| awk '{printf "%s %s %6s %6s %4s %7s %4s %5s %7s %9s %11s %3s %s\n", $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13}' >> evtlist.txt 
        fi
done


