#!/bin/bash

# Entre com o ano em frente ao script na linha de comando
year=$1

phase=P
#phase=PKIKP

if [ "$phase" = "P" ]
then
    deltamin=30
    deltamax=95
    magmin=4.5
elif [ "$phase" = "PKIKP" ]
then
    deltamin=150
    deltamax=180
    magmin=5.0
fi

cat /home/marcelo/maps/a-sta/StaList.all | grep Antarctica | while read id net sta lat lon elev b e loc status
do

   if test -f $net-$sta-$year-$phase.list; then
      echo $net-$sta-$year-$phase".list Exist!"
   else

      byear=`echo $b | sed 's/\// /g' | awk '{print $1}'`

      if [ $year -ge $byear ]; then  

         for daymin in 001 074 147 220 293
         do 
            daymax=`expr $daymin + 73`

            echo $year $daymin $daymax $phase $deltamin $deltamax $magmin $net $sta $lat $lon $elev

            get-evlist.py -b $year-$daymin -e $year-$daymax -l $magmin -m 10 --rmin=$deltamin --rmax=$deltamax --lat=$lat --lon=$lon -s 3
            mv evlist.txt $sta-$year-$phase-$daymin-$daymax.list

         done

         cat  $sta-$year-$phase-*.list > tmp
         rm $sta-$year-$phase-*.list
         sort tmp | awk '{if ($0 != prev) {print; prev = $0}}' > $net-$sta-$year-$phase.list
         rm tmp
      else
         echo "------------------------------"
         echo "Station no have year: "$year
         echo "------------------------------"
      fi
   fi

done
