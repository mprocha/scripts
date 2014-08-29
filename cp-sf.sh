#!/bin/bash

file=$1


sudo cp -pr /media/sf_Desktop/$file ~
sudo chown -R sismologo:sismologo ~/$file

echo "Arquivo "$1" copiado para HOME do usuario"
