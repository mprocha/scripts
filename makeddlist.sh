#!/bin/bash

# New script for generate dd.list
# Marcelo Rocha 2015/09/07

ls -1 *.sac | awk '{print substr($0,1,17)}' | awk '{ if ($1 != prev ) {print; prev = $1 }}' | awk '{print "./dd "$1"*.1.sac"}' > ./dd.list

echo " "
echo "dd.list file was created!!!"
echo " "
