#!/bin/bash
dd=`date +%Y-%m-%d-%H-%m-%S`
logfile=logfile-$dd.log

> /storage3/Bkp-SDS/$logfile
begin=`date`
echo "Incio: "$begin  >> $logfile

rsync -av --progress --inplace --log-file="/storage3/Bkp-SDS/rsync.log.$dd" /SDS /storage3/Bkp-SDS

end=`date`
echo "Fim  : "Eend  >> $logfile
