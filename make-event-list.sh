#!/bin/bash

usage(){
if [ -z $1 ]
then
   echo " "
   echo "usage: make-event-list.sh year phase "
   echo " "
   echo "   Use the following Phase Names:"
   echo "    P, PKIKP, S, ScS, SKS, SKKS"
   echo " "
fi
}

if [ -z $1 ]
then
   usage
   exit 1
fi

# Entre com o ano em frente ao script na linha de comando
year=$1
phase=$2


#phase=P
#phase=PKIKP
#phase=S ## phase ScS have the same GCARC interval than S
#phase=SKS
#phase=SKKS

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
elif [ "$phase" = "S" ]
then
    deltamin=30
    deltamax=95
    magmin=5.4
elif [ "$phase" = "ScS" ]
then
    deltamin=30
    deltamax=95
    magmin=5.4
elif [ "$phase" = "SKS" ]
then
    deltamin=100
    deltamax=145
    magmin=5.4
elif [ "$phase" = "SKKS" ]
then
    deltamin=100
    deltamax=180
    magmin=5.4
else
    echo " "
    echo "Type a correct phase name"
    usage    
    exit 1
fi


echo "Phase: "$phase"   Deltamin: "$deltamin"   Deltamax: "$deltamax"   Magmin: "$magmin

latMin=-40
latMax=6
lonMin=-74
lonMax=-30

cat /home/marcelo/maps/a-sta/StaList.all | grep -v sugerida | grep -v planejada | grep -v verificar | awk '{ if ( $4 >= -40 && $4 <= 6 && $5 >= -74 && $5 <= -30 ) { print $0 } }' | while read id net sta lat lon elev b e loc status
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
         echo "-------------------------------------------"
         echo "Station "$sta" no have data for year "$year
         echo "-------------------------------------------"
      fi
   fi

done
