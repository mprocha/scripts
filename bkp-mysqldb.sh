#!/bin/bash

# Script to generate a backup of all databases in a mysql
# database server:
# Marcelo Rocha - UnB - 2014/04/21 - V1.0

date=`date --rfc-3339=date`
dir=~/Bkp-mysqldb

echo "  "

if test -d $dir
then
   echo "Directory "$dir" Exist!!!"
else
   mkdir $dir
   echo "Directory "$dir" Created!!!"
fi

if test -f $dir/backup-$date.sql.gz
then
   rm $dir/backup-$date.sql.gz
   echo $dir/backup-$date.sql.gz" REMOVED!!"
fi

echo "  "
echo "Type mysql user password!!!"
mysqldump -u root -p -x -e -A > $dir/backup-$date.sql
gzip $dir/backup-$date.sql

echo "  "
echo "A new MYSQLDB ("backup-$date.sql.gz") backup was created in dir "$dir
echo "  "
