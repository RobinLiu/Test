#!/bin/bash
ssh tcu-1 " node start /root/uda0.0114_1 /tmp/dmp/dsp19.conf 0x0013ffff"
ssh tcu-1 "node status 0x0013ffff"
/etc/init.d/linxToDSP.sh start
fshascli -rn /SGWNetMgr /SS7SGU 
sleep 2
fshascli -rn /MGW_CMRG
tail -f /srv/Log/log/syslog | grep srm
#tail -f /srv/Log/log/syslog | grep srm 
#filename=`date`.cap
#ssh cla-1 "filename=`date`; tcpdump -i eth2 -s 0 -w ${filename}.cap ether proto 0x8901"

