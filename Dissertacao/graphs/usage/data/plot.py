#!/bin/python
#get all files in directory
from os import listdir, mkdir, rmdir, makedirs
from os.path import isfile, join, exists, isdir
from shutil import rmtree
import os
from os.path import join, basename


import re
from numpy import *
import Gnuplot, Gnuplot.funcutils




DATA_DIRECTORY = "./results"
OUTPUT_DIRECTORY ="./graphs"

if not exists(OUTPUT_DIRECTORY):
	makedirs(OUTPUT_DIRECTORY)


cast={'web':'Cassandra II + Voldemort II',
		  'database':'Voldemort I',
		  'proxy':'HA Proxy + Proxy',
		  'client':'Replay Instance I + TryOut',
		  'manager':'Manager + Cassandra I + Replay II',
		  'server1':'Server I ',
		  'database2':'Server II ',
		  'web1':'Server III ',
		  'web2':'Server IV ',
		  'web3':'Server V ',
		  'web4':'Server VI ',
		  }


def pretify(parameter):
	if parameter == "CPUUtilization":
		return "CPU Utilization",'\%'

	param = re.sub(r"(\w)([A-Z])", r"\1 \2", parameter)
	parts = param.split(' ')
	if parts[0] == "Network":
		return param,'MBytes'
	return parts[0]+parts[1],parts[2]





def plot(stat,parameter,instances):
	parameterTitle,unit = pretify(parameter)
	

	g = Gnuplot.Gnuplot(debug=1)
	g("set terminal pngcairo dashed")
	g("set terminal epslatex dashed")
	g("set xlabel 'Time (Hour:Minute)'")
	g('set timefmt "%H:%M"')
	g('set yrange [ 0 : ]')
	g('set xdata time')
	g('set xrange ["00:00":"10:00"]')
	g('set xtics "2:00"')
	g("set key outside top right width -5 height 0.8 spacing 1.3")
	g('set style line 1 lw 2 lt 1 ps 2 pt 3 lc rgb "black" pointinterval 20')
	g('set style line 2 lw 2 lt 2 ps 2 pt 4 lc rgb "black" pointinterval 20')
	g('set style line 3 lw 1 lt 1 ps 2 pt 1 lc rgb "black" pointinterval 20')
	g('set style line 4 lw 2 lt 1 ps 2 pt 6 lc rgb "black" pointinterval 20')
	g('set style line 5 lw 2 lt 1 ps 2 pt 5 lc rgb "black" pointinterval 20')

	# 63A52C, 
	# BE2F00 #orange
	# 003060 #blue
	# F99500 #yellow
	# 7878A5
	# C5172C #red
	# 42443C #dark green
	# 63A52C #light green

	if unit == "%":
	  	g('set yrange [0:100]')

 	g('set ylabel "'+stat+' '+parameterTitle+' ('+unit+')"')

	
	g("set output '"+OUTPUT_DIRECTORY+"/"+stat+'_'+parameter+'.tex')

	plot="plot "
	i = 1
	for name in instances:
		plot = plot+'"'+DATA_DIRECTORY+"/"+parameter+"/"+stat+"/"+name+".txt"

		if unit == "MBytes":
			plot = plot + '" using 1:($2/1000000)'
		else:
			plot = plot + '" using 1:2'

		plot = plot + " with linespoints title '"+cast[name]+"' ls "+str(i)+', '
		i = i + 1
	g(plot)


#plot("Maximum", "CPUUtilization", ["proxy","client","manager"])
plot("Maximum", "CPUUtilization", ["database2","web1","web2","web3","web4"])



# cast={'web':'Cassandra II + Voldemort II (xlarge)',
# 		  'database':'Voldemort I (xlarge)',
# 		  'proxy':'HA Proxy + Proxy (xlarge)',
# 		  'client':'Replay Instance I + TryOut (xlarge)',
# 		  'manager':'Manager + Replay Instance II (xlarge) + Cassandra I',
# 		  'server1':'Application Server I (large)',
# 		  'database2':'Application Server II (large)',
# 		  'web1':'Application Server III (large)',
# 		  'web2':'Application Server IV (large)',
# 		  'web3':'Application Server V (large)',
# 		  'web4':'Application Server VI (large)',


#results/NetworkOut/Minimum/web4.txt
