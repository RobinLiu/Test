#!/bin/sh
if [ $# != 2 ] 
then
	echo "usage: $0  CM_PHY_ADDR LOG_LEVEL"
	echo "Example:"
	echo "$0  0700 3"
	exit 0
fi

old_config=$GET_CONFIG
old_phy_add=$LIBGEN_USE_PHYS_ADDR
export GET_CONFIG="/etc/LibgenConfig_CM.ini"
export LIBGEN_USE_PHYS_ADDR=$1
dmxsend -- -h 1A,*,a26,00,00,00,00,6034,00 -b 1,$2
dmxsend -- -h 1A,*,a27,00,00,00,00,6034,00 -b 1,$2
export GET_CONFIG=$old_config
export LIBGEN_USE_PHYS_ADDR=$old_phy_add
