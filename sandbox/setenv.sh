#!/bin/sh
if [ $# != 1 ] 
then
	echo "usage: $0 [latest/angelina/lima]."
	exit 0;
fi

if [ $1 == 'latest' ] 
then
	echo "use latest env"
	cd ~/atcamgw-main/product/build/
	rm -rf platform_settings.source 
	rm -rf set_dmxsee.source
	svn up
elif [ $1 == 'angelina' ]
then
	echo "use the angelina evn"
	cd ~/atcamgw-main/product/build/
	cp platform_settings.source.ok platform_settings.source
	cp set_dmxsee.source.ok set_dmxsee.source
elif [ $1 = "lima" ]
then
	echo "use lima env."
	rm -rf platform_settings.source
	rm -rf set_dmxsee.source
	svn up
	cd ~/atcamgw-main/product/build/
	cp platform_settings.source.lima  platform_settings.source
	#cp set_dmxsee.source.lima set_dmxsee.source
fi

cd ~/atcamgw-main/SS_MGWSGWRM/build
~/atcamgw-main/product/build/svnenv.sh -w -a x86_64
