#!/bin/bash

file=$1


sudo cp /media/sf_Desktop/$file ~
sudo chown -R sismologo:sismologo ~/$file

ls -l ~

echo "Arquivo copiado"
