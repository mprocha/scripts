#!/bin/bash

dd=`date +%Y-%m-%d-%H-%m-%S`
logfile=logfile-$dd.log
dir=/SDS-BKP/

> $dir/$logfile
begin=`date`
echo "Incio: "$begin  >> $dir$logfile

rsync -av --progress --inplace --log-file="/SDS-BKP/rsync.log.$dd" /SDS/ $dir

end=`date`
echo "Fim  : "$end  >> $dir$logfile
