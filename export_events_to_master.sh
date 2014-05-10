#!/bin/bash

FROM_DB="-d postgresql://sysop:sysop@10.110.0.130/master_sc3"
TO_DB="-d postgresql://sysop:sysop@10.110.0.130/sc_master"

START="2013-07-30 00:00:00"
END="2013-08-01 00:00:00"

for evt in $(seiscomp exec scevtls $FROM_DB --begin "${START}" --end "${END}"); do
	echo exporting $evt
	seiscomp exec scxmldump  $FROM_DB  -fPAMF -E $evt | \
	seiscomp exec scdb --plugins dbpostgresql -i -  $TO_DB --debug
done


#for evt in $(seiscomp exec scevtls $FROM_DB --begin "${START}" --end "${END}"); do
#	echo exporting $evt
#	seiscomp exec scxmldump  $FROM_DB  -fPAMF -E $evt > ${evt}.xml
#done

