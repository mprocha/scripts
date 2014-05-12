#!/bin/bash

# Script to generate a backup of SDS directory
# Marcelo Rocha - UnB - 2014/05/11 - V1.0

dirlocal=`pwd`

dir=/storage3/Bkp-SDS

date=`date --rfc-3339=date` 
dirbkp=SDS-$date


if test -d $dirbkp
then
   echo "Directory "$dirbkp" Exist!!!"
   rm  -r $dirbkp/*
else
   mkdir $dirbkp
   echo "Directory "$dirbkp" Created!!!"
fi

cp -pr /SDS/* $dir/$dirbkp

cd $dirlocal 
