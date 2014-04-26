#!/bin/bash

date=`date`

git init
git add .
git commit -m "Atualização $date"
git push origin master
