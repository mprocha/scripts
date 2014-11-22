#!/bin/bash

date=`date`

read -p "Digite o comentario sobre as modificações feitas: " comment


#git init
git add .
git commit -m "Atualização $date: $comment"
git push origin master
