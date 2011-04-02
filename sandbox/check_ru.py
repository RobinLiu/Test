#!/usr/bin/python
import os
from subprocess import Popen, PIPE, STDOUT
import time
import re
import telnetlib
from get_sys_info import get_node_list, get_spec_node_list, get_active_tcu, get_ru_list, is_active_ru
g_rg_list = [
			'/SGWNetMgr',
			'/SS7SGU',
			'/MGW_CMRG',
			'/MGW_OMURG',
			'/Directory',
]

status_dict={
	"administrative":	"UNLOCKED",
	"operational":		"ENABLED",
	"usage":			"ACTIVE",
	"procedural":		'',
	"availability":		'',
	"unknown":			"FALSE",
	"alarm":			'',
	"role":				"ACTIVE"
}

def get_mo_status(mo_name):
	cmd = 'fshascli -s ' + mo_name
	output = os.popen(cmd).readlines()
	mo_status = {}
	for line in output:
		if len(line) > 1:
			p = re.compile(r'(\S*)\((\S*)\)')
			m = p.search(line)
			if m:
				mo_status[m.group(1)] = m.group(2)
	return mo_status


def cmp_mo_status(mo_status):
	ret = True
	error_info = ''
	for k, v in mo_status.items():
		if k != 'role' and status_dict[k] != v :
			error_info = "    " + k + " should be \"" + status_dict[k] + "\" But is \"" + v +"\""
			ret = False
			return ret, error_info
	return ret, error_info

def is_ru_active(mo_status):
	return 'role' in mo_status and mo_status['role'] == 'ACTIVE'

	
def check_mo_status(mo_name, mo_status):
	status, error_info = cmp_mo_status(mo_status)
	if status:
		print("%-40s OK"%(mo_name))
	else:
		print("%-40s NOK:"%(mo_name))
		print(error_info)
	return status
		

def check_mo_list(ru_list):
	status = True
	for ru in ru_list:
		mo_status = get_mo_status(ru)
		if is_ru_active(mo_status):
			status = check_mo_status(ru, mo_status) and status
	return status
		
	
def check_rg_status(rg_name):
#	print("start to check RG " + rg_name + " ...")
	mo_status = get_mo_status(rg_name)
	status = check_mo_status(rg_name, mo_status)

	if status:
		ru_list = get_ru_list(rg_name)
		if ru_list:
			status = check_mo_list(ru_list) and status
	return status


def check_clock():
	cmd = 'fsclish -c "show mgw synchronization inputreference"'
	ret = os.popen(cmd).read()
	print(ret)
	r_list = ret.split()
	if 'yes' in r_list and 'ok' in r_list:
		print("Clock is ok")
		return True
	else:
		print "================================================================="
		print "CLOCK IS NOT OK !!!"
		print "================================================================="
		return False

def is_needed_node_available(node_list):
	num_tcu = 0
	num_tdm = 0
	num_cla = 1
	for node in node_list:
		if node.startswith("TCU"):
			num_tcu += 1
		if node.startswith("TDM"):
			num_tdm += 1
#		if node.startswith("CLA"):
#			num_cla += 1
	if num_tcu == 0:
		print "No Working DSP available"
	if num_tdm == 0:
		print "No Working TDM available"
	if num_cla == 0:
		print "No Working CLA available"
	return num_tcu and num_cla and num_tdm

def check_needed_rg(rg_list):
	result = True
	for rg in rg_list:
		result = check_rg_status(rg) and result
	return result
	
def check_node():
	result = True
	node_list = get_node_list()	
	if not is_needed_node_available(node_list):
		print "Please first make the node working!"
		return
	for node in node_list:
		if not check_rg_status("/"+node):
			result = False	
	return result

def check_node_list(node_list):
	result = True
	for node in node_list:
		result = check_rg_status("/"+node) and result
	return result

	
def check_all(node_list_all):
	ret = True
	ret = check_needed_rg(g_rg_list) and ret 
	ret = check_node_list(node_list_all) and ret
	ret = check_clock() and ret 
	return ret
	
def check_for_link(node_list_all):
	tcu_list = get_spec_node_list(node_list_all, "TCU")
	tdm_list = get_spec_node_list(node_list_all, "TDM")
	active_tcu_list = get_active_tcu(tcu_list)
	ret = True
	ret = check_node_list(tdm_list) and ret
	ret = check_node_list(active_tcu_list) and ret
	ret = check_needed_rg(g_rg_list) and ret
	check_clock()
	return ret


from optparse import OptionParser

if __name__ == '__main__':
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-a", "--all",
                      action="store_true", dest="check_all_flag",
                      default=False)
    opts, args = parser.parse_args()
    node_list = get_node_list()
    ret = False
    if(opts.check_all_flag):
	    ret = check_all(node_list)
    else:
        ret = check_for_link(node_list)
#		os.system('tail -f /srv/Log/log/syslog | grep srm')
    if ret:
        print ("Check ok")
    else:
		print("Not all check passed, please first check the RU and clock status")
