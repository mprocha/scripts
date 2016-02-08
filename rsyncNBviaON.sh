#!/bin/bash

for i in `seq 2010 2016`
do
   if [ -d $i ]
   then
      echo "Diretorio "$i" existe"
   else
      mkdir $i
   fi
   cd $i
   sshpass -p "on2014sds" rsync -av --timeout=50 on@rsis2.on.br::NB/$i/  ./
   cd ..
done
