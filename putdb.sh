#!/bin/bash

for ev in *.xml
do
scdb -i $ev -d mysql://sysop:sysop@localhost/seiscomp3 -b 1000
done
