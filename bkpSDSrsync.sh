#!/bin/bash

dd=`date +%Y-%m-%d-%H-%m-%S`
logfile=logfile-$dd.log
dir=/storage3/Bkp-SDS

> $dir/$logfile
begin=`date`
echo "Incio: "$begin  >> $dir/$logfile

rsync -av --progress --inplace --log-file="/storage3/Bkp-SDS/rsync.log.$dd" /SDS $dir

end=`date`
echo "Fim  : "$end  >> $dir/$logfile
