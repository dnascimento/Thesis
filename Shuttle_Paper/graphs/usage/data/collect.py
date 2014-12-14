#!/bin/python
import os
instances=['i-eb0a4f0a','i-3f3570de','i-119be1f0','i-ad142a43','i-e7befb06','i-075613e6','i-c6ef8e28','i-c4ef8e2a','i-c2ef8e2c','i-c3ef8e2d','i-e3d1af02']
names=['web1','web2','database2','manager','web3','web4','database','web','proxy','client','server1']

metrics=["CPUUtilization","DiskReadOps","DiskReadBytes","NetworkOut","NetworkIn","DiskWriteOps","DiskWriteBytes"]
stats="Maximum"

for metric in metrics:
	for i in range(len(instances)):
		instance = instances[i]
		name = names[i]
		command = "aws cloudwatch get-metric-statistics --metric-name "+metric+" --start-time 2014-11-26T00:00:00 --end-time 2014-11-26T23:59:59 --period 300 --namespace AWS/EC2 --statistics "+stats+" --dimensions Name=InstanceId,Value="+instance+" > "+metric+"_"+stats+"_"+instance+"_"+name+".txt"
		print command
		os.system(command)