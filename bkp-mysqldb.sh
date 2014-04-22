#!/bin/bash

# Script to generate a backup of all databases in a mysql
# database server:
# Marcelo Rocha - UnB - 2014/04/21 - V1.0

par1=$1
par2=$2

usage(){
   echo " "
   echo "bkp-mysqldb.sh: "
   echo "Script to generate a backup of database"
   echo "in a mysql database server."
   echo " "
   echo "Marcelo Rocha - UnB - 21-04-2013 - V1.0"
   echo "email: marcelorocha.unb@gmail.com"
   echo " "
   echo "Usage:"
   echo "bkp-mysqldb.sh [flag] [arg]"
   echo " "
   echo "flags:"
   echo "-h         Show this mensage"
   echo "-f <file>  Option to choose the output file name"
   echo "           Default (without arg): backup-yyyy-mm-dd.sql"
   echo " "
   echo "The file is gziped and saved in the directory ~/Bkp-mysqldb"
   echo " "
} 

if [ $par1 = "-h" ]
then
   usage
   exit 1
elif [ -z $par1 ]
then
   usage
   exit 1
elif [ $par1 = "-f" ]
then
   if [ -z $par2 ]
   then   
      date=`date --rfc-3339=date`
      file=backup-$date.sql
   else
      file=$par2
   fi
fi

dir=~/Bkp-mysqldb

echo " "

if test -d $dir
then
   echo "Directory "$dir" Exist!!!"
else
   mkdir $dir
   echo "Directory "$dir" Created!!!"
fi

if test -f $dir/$file.gz
then
   rm $dir/$file.gz
   echo "OLD FILE "$dir"/"$file".gz WAS REMOVED!!"
fi

echo " "
echo "Type mysql user password!!!"
mysqldump -u root -p -x -e -A > $dir/$file
gzip $dir/$file

echo "  "
echo "A new MYSQLDB ("$file".gz) backup was created in dir "$dir
echo "  "
