#!/bin/bash

for i in `seq 1988 2016`
do
#   if [ -d $i ]
#   then
#      echo "Diretorio "$i" existe"
#   else
#      mkdir $i
#   fi
#   cd $i
   
   sshpass -p "unb2014sds" rsync -av unb@200.144.254.162::BL/$i ./

#   cd ..
done
