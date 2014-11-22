#!/usr/bin/python

from os import getcwd, walk, sep, rename

workspace = getcwd()

tree = walk(workspace)

for root, dirs, files in tree :
	for file in files :
		if file[-5:] == '.seed' :
			param = file.split(".")			
			sta = param[1]
			if len(sta) == 5 :				
				rename(root+sep+file, root+sep+file[:24])
				print 'renomeando '+file+' para '+file[:24]+' ...ok!'
			else :				
				rename(root+sep+file, root+sep+file[:23])
				print 'renomeando '+file+' para '+file[:23]+' ...ok!'

