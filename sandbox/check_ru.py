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

def build_correct_result(ru_name):
	correct_result = []
	correct_result.append(ru_name + ':\n')
	correct_result.append('administrative(UNLOCKED)\n')
	correct_result.append('operational(ENABLED)\n')
	correct_result.append('usage(ACTIVE)\n')
	correct_result.append('procedural()\n')
	correct_result.append('availability()\n')
	correct_result.append('unknown(FALSE)\n')
	correct_result.append('alarm()\n')
	return correct_result
	
def build_correct_ru_result(ru_name):
	correct_result = []
	correct_result = build_correct_result(ru_name)
	correct_result.append('role(ACTIVE)\n')
	return correct_result
	
	
def check_result(correct_result, output):
	i = len(correct_result)
	error_info = ''
	result = True
	for index in range(i):
		try:
			if correct_result[index] != output[index]:
				error_info ="\tStatus should be: " + correct_result[index] +"\tBut is "+ output[index]
				result = False
		except IndexError:
			result = False
			error_info = output
	return result, error_info
		

def check_ru(ru_name):
	cmd = 'fshascli -s ' + ru_name
	output = os.popen(cmd).readlines()
	status, error_info = check_result(build_correct_ru_result(ru_name), output)
	if status:
		print("%-40s OK"%(ru_name))
	else:
		print("%-40s NOK:"%(ru_name))
		print(error_info)
	return status

def check_ru_list(ru_list):
	status = True
	for ru in ru_list:
		if is_active_ru(ru):
			status = check_ru(ru) and status
	return status
		
	
def check_rg_status(rg_name):
#	print("start to check RG " + rg_name + " ...")
	cmd = 'fshascli -s ' + rg_name
	output = os.popen(cmd).readlines()
	status, error_info = check_result(build_correct_result(rg_name), output)
	if status:
		print("%-40s OK"%(rg_name))
		ru_list = get_ru_list(rg_name)
		if ru_list:
			status = check_ru_list(ru_list) and status
	else:
		print("%-40s NOK"%(rg_name))
		print(error_info)
	return status

def check_clock():
	try:
		p = Popen(["fsclish"], shell=False, stdin=PIPE, stdout=PIPE)
#		time.sleep(1)
		p.stdin.write("show mgw synchronization inputreference\n")
#		time.sleep(1)
		p.stdin.write("quit\n")
		ret = p.stdout.read()
	except IOError:
		print ("--IOError")
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


if __name__ == '__main__':
	node_list = get_node_list()
	# if check_for_link(node_list):
	if check_all(node_list):
		os.system('tail -f /srv/Log/log/syslog | grep srm')
	else:
		print("Not all check passed, please first check the RU and clock status")
