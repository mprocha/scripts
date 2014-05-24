#!/bin/bash

dd=`date +%Y-%m-%d-%H-%m-%S`
logfile=logfile-$dd.log
dir=/storage2/Bkp-SDS

> $dir/logs/log-files/$logfile
begin=`date`
echo "Incio: "$begin  >> $dir/logs/log-files/$logfile

rsync -av --progress --inplace --log-file="/storage3/Bkp-SDS/logs/log-rsync/rsync.log.$dd" /SDS $dir

end=`date`
echo "Fim  : "$end  >> $dir/logs/log-files/$logfile
