#!/bin/bash

for i in `seq 2010 2014`
do
   if [ -d $i ]
   then
      echo "Diretorio "$i" existe"
   else
      mkdir $i
   fi
   cd $i
   sshpass -p "unb2014sds" rsync -av --timeout=50 unb@rsis2.on.br::ON/$i/  ./
   cd ..
done
