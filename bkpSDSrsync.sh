#!/bin/bash
dd=`date +%Y-%m-%d-%H-%m-%S`
rsync -av --progress --inplace --log-file="/storage3/Bkp-SDS/rsync.log.$dd" /home/suporte/tmp /storage3/Bkp-SDS
