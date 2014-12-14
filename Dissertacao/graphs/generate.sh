#/bin/bash

subpath()
{
    echo "$1" | rev | cut -d"/" -f1-$2 | rev
}

fixGnuplot(){
	cd $1
	if [ -f generate* ]; then
		gnuplot generate*
		MY_PATH=$(pwd)
		BASE=$(subpath $MY_PATH 2)
		for f in *.tex
		do
			echo "$f"
			NAME=$(basename $f .tex)
			mv $f $f.back
			sed "s|${NAME}|${BASE}/${NAME}|" $f.back > $f
			rm $f.back
		done
	fi
	cd ..
}








for d in */ ; do
    fixGnuplot $d
done




