#!/usr/bin/python
import os
from check_ru import check_for_link
from clear_res import clear_all
from get_sys_info import get_node_list, get_spec_node_list, get_active_tcu 

print ("call check_all ")

node_list = get_node_list()
if check_for_link(node_list):
	print("All Check is ok")
	print ("Start to create Link......")
	tcu_list = get_spec_node_list(node_list, "TCU")
	tdm_list = get_spec_node_list(node_list, "TDM")
	active_tcu_list = get_active_tcu(tcu_list)
	clear_all(tdm_list, active_tcu_list)
	os.system('tail -f /srv/Log/log/syslog | grep srm')
else:
	print("Not all check passed, check it first!!!")
        print ("Start to create Link......")
        tcu_list = get_spec_node_list(node_list, "TCU")
        tdm_list = get_spec_node_list(node_list, "TDM")
        active_tcu_list = get_active_tcu(tcu_list)
        clear_all(tdm_list, active_tcu_list)
        os.system('tail -f /srv/Log/log/syslog | grep srm')
