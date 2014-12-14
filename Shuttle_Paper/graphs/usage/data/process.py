#!/bin/python
import json
from pprint import pprint

#get all files in directory
from os import listdir, mkdir, rmdir, makedirs
from os.path import isfile, join, exists
from shutil import rmtree


mypath = "./"
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

if exists("./output"):
	rmtree("output")
mkdir("output")

def parse(fName):
	fNameParts=fName.split("_")
	PARAMETER=fNameParts[0]
	PARAMETER_STATS=fNameParts[1]
	INSTANCE_CODE=fNameParts[2]
	INSTANCE_NAME=fNameParts[3]
	outputDir = "output/"+PARAMETER+"/"+PARAMETER_STATS
	if not exists(outputDir):
		makedirs(outputDir)
	out = open(outputDir+"/"+INSTANCE_NAME,'w+')
	print fName
	#read file to JSON
	json_file = open(fName)
	json_data = json.load(json_file)

	data={}

	for point in json_data['Datapoints']:
		time = point['Timestamp']
		value = point[PARAMETER_STATS]
		data[time] = value

	for key in sorted(data):
		timeParts = key.split("T")[1].split(":")
		hour = int(timeParts[0])-9
		minute = timeParts[1]
		out.write("%s:%s  %s\n" % (hour,minute, data[key]))


	out.close()
	json_file.close()


for f in onlyfiles:
	if f[0] is not '.' and f[-2:] != "py":
		parse(f)


