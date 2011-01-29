#!/usr/bin/python
import os
from subprocess import Popen, PIPE, STDOUT
import time
import re
import telnetlib
from get_sys_info import get_node_list, get_spec_node_list, get_active_tcu 

def clear_tdm_resc(tdm_node):
	os.system('killall telnet')
	os.system('ssh '+ tdm_node + ' "killall telnet"')
	try:
		tn = telnetlib.Telnet()
	except IOError :
		print("err: ")
	if tn:
		tn.set_debuglevel(10)
		try:
			tn.open(tdm_node, 2999)
			tn.read_until(">")
		except Error:
			print ("error")
		print("telnet ok")
	else:
		print("telnet nok")
	tn.write("show show_res\r\n")
	tn.read_until('>')

	tn.write("config clear_all \r\n")
	tn.read_until('>')

	tn.write("show show_res\r\n")
	tn.read_until('>')
	print "-------------"
	tn.write("exit \r\n")

def clear_all_tdm_res(tdm_node_list):
	for tdm_node in tdm_node_list:
		clear_tdm_resc(tdm_node)

def restart_dsp_core(tcu_node):
	print "Restart TCU:" + tcu_node
	os.system('ssh '+ tcu_node + ' " node start /root/uda0.0114_1 /tmp/dmp/dsp19.conf 0x0013ffff"')
	os.system('ssh ' + tcu_node +' "node status 0x0013ffff"')

def restart_all_sgw_dsp_core(tcu_node_list):
	for tcu_node in tcu_node_list:
		restart_dsp_core(tcu_node)

def clear_all(tdm_node_list, tcu_node_list):
	clear_all_tdm_res(tdm_node_list)
	restart_all_sgw_dsp_core(tcu_node_list)
	os.system('/etc/init.d/linxToDSP.sh start')
	os.system('fshascli -rn /SGWNetMgr /SS7SGU ')
	time.sleep(2) 
	os.system('fshascli -rn /MGW_CMRG')

if __name__ == '__main__':
	node_list = get_node_list()
	tcu_list = get_spec_node_list(node_list, "TCU")
	tdm_list = get_spec_node_list(node_list, "TDM")
	active_tcu_list = get_active_tcu(tcu_list)
	clear_all(tdm_list, active_tcu_list)