#!/bin/bash

dd=`date +%Y-%m-%d-%H-%m-%S`
logfile=logfile-$dd.log
dir=/SDS-BKP/

> $dir/log-rsync/$logfile
begin=`date`
echo "Incio: "$begin  >> $dir/log-rsync/$logfile

rsync -av --progress --inplace --log-file="/SDS-BKP/log-rsync/rsync.log.$dd" /SDS/ $dir

end=`date`
echo "Fim  : "$end  >> $dir/log-rsync/$logfile
