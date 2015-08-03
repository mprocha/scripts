#!/bin/bash

VERIFICA=$(df -h | awk '{ print $1}' | grep 164.41.28.155:/nfs/SDS)

if [ $VERIFICA = 164.41.28.155:/nfs/SDS ]; then

dd=`date +%Y-%m-%d-%H-%m-%S`
logfile=logfile-$dd.log
dir=/SDS-BKP/

> $dir/log-rsync/$logfile
begin=`date`
echo "Incio: "$begin  >> $dir/log-rsync/$logfile

rsync -av --exclude="/SDS/SDS_SIS" --progress --inplace --log-file="/SDS-BKP/log-rsync/rsync.log.$dd" /SDS/ $dir

end=`date`
echo "Fim  : "$end  >> $dir/log-rsync/$logfile

fi
