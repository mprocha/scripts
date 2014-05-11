#!/bin/bash

# Script to generate a backup of all events (xml) of the seiscomp databases
# Marcelo Rocha - UnB - 2014/05/11 - V2.0

usage(){
   echo " "
   echo "Script to generate a backup of all events (xml)"
   echo "of the seiscomp databases"
   echo " "
   echo "Marcelo Rocha - UnB - 11-05-2013 - V2.0"
   echo "email: marcelorocha.unb@gmail.com"
   echo " "
   echo "Usage:"
   echo "bkpXMLdb.sh [flag] [arg]"
   echo " "
   echo "flags:"
   echo "-h                   Show this mensage"
   echo "-db <database name>  Option to choose the output file name"
   echo "                     Default (without arg): seiscomp3"
   echo "                     Possible database name: sc3_master"
   echo " "
   echo "The files will be saved in the directory /SDS/Bkp-seiscompXMLdb"
   echo " "
}

par1=$1
par2=$2
dirlocal=`pwd`

if [ -z $par1 ]
then
   usage
   exit 1
elif [ $par1 = "-h" ]
then
   usage
   exit 1
elif [ $par1 = "-db" ]
then
   if [ -z $par2 ]
   then
      db=seiscomp3
   else
      db=$par2
   fi
fi

cd /SDS
echo " "

dbfile=evdb.dat

dir=Bkp-seiscompXMLdb
if test -d $dir
then
   echo "Directory "$dir" exist in /SDS"
else
   mkdir $dir
   echo "Directory "$dir" created in /SDS"
fi

cd $dir

dirhost=`hostname`
if test -d $dirhost
then
   echo "Directory "$dirhost" Exist!!!"
else
   mkdir $dirhost
   echo "Directory "$dirhost" Created!!!"
fi

echo " "
cd $dirhost

date=`date --rfc-3339=date` 
direv=evxml-$date
mkdir $direv
cd $direv

scevtls -d mysql://sysop:sysop@localhost/$db --begin "2009-01-01 00:00:00" --end "$date 23:59:59" > $dbfile

cat $dbfile | while read ev
do
   scxmldump -d mysql://sysop:sysop@localhost/$db -E $ev -PAMf -o $ev.xml
done

rm $dbfile
echo " "
echo XML-files send to /SDS/$dir/$dirhost/$direv

cd $dirlocal 
