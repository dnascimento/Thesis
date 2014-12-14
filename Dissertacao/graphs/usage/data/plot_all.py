#!/bin/python
#get all files in directory
from os import listdir, mkdir, rmdir, makedirs
from os.path import isfile, join, exists, isdir
from shutil import rmtree
import os
from os.path import join, basename


import re
from numpy import *
# If the package has been installed correctly, this should work:
import Gnuplot, Gnuplot.funcutils




#Go to each directory
mypath = "./"

cast={'web':'Cassandra II + Voldemort II (xlarge)',
		  'database':'Voldemort I (xlarge)',
		  'proxy':'HA Proxy + Proxy (xlarge)',
		  'client':'Replay Instance I + TryOut (xlarge)',
		  'manager':'Manager + Replay Instance II (xlarge) + Cassandra I',
		  'server1':'Application Server I (large)',
		  'database2':'Application Server II (large)',
		  'web1':'Application Server III (large)',
		  'web2':'Application Server IV (large)',
		  'web3':'Application Server V (large)',
		  'web4':'Application Server VI (large)',
		  }


def pretify(parameter):
	if parameter == "CPUUtilization":
		return {'param':"CPU Utilization",'unit':'%'}

	param = re.sub(r"(\w)([A-Z])", r"\1 \2", parameter)
	parts = param.split(' ')
	if parts[0] == "Network":
		return {'param':param,'unit':'Bytes'}
	return {'param':parts[0]+parts[1],'unit':parts[2]}

def plot(root,files):
	stat = root.split("/")[-1]
	param = pretify(root.split("/")[-2])
	
	

	g = Gnuplot.Gnuplot(debug=1)
	g("set terminal pngcairo")
	g("set xlabel 'Time'")
	g('set timefmt "%H:%M"')
	g('set yrange [ 0 : ]')
	g('set xdata time')

	g("set key top right box  height 0.8 width -5 spacing 1.3")
	g('set style line 1 lw 1 lt 1 ps 2 pt 3 lc rgb "#42443C"')
	g('set style line 2 lw 1 lt 1 ps 2 pt 4 lc rgb "#C5172C"')
	g('set style line 3 lw 1 lt 1 ps 2 pt 4 lc rgb "black"')
	g('set style line 4 lw 2 lt 1 ps 2 pt 4 lc rgb "#63A52C"')

	if param['unit'] == "%":
		g('set yrange [0:100]')
	if param['unit'] == "Bytes":
		param['unit'] = "MBytes"

	g('set ylabel "'+stat+' '+param['param']+' ('+param['unit']+')"')

	
	folder = "resultGraphsInd"
	#g("set output '"+folder+"/"+stat+'_'+param+'.png')
	if not exists(folder):
		makedirs(folder)


	plot="plot "
	i = 1
	for f in files:
		name = f[:-4]
		plot = plot+'"'+root+"/"+f
		if param['unit'] == "MBytes" :
			plot = plot + '" using 1:($2/1000000)'
		else:
			plot = plot + '" using 1:2'

		plot = plot+' with line title "'+cast[name]+'" ls '+str(i)+", "
		g("set output '"+folder+"/"+stat+'_'+param['param']+"_"+name+'.png')
		g(plot)

		plot="plot "
		i = i + 1
	g(plot)




for root, dirs, files in os.walk('./results'):
	selectedFiles = []
	for f in files:
		if f[0] != '.' and f[-2:] != "py" and f[-3:] != "png":
			selectedFiles.append(f)

	files = selectedFiles

	if len(files) is not 0:
		print "plotting",root," : ",len(files), " files"
		plot(root,files)







