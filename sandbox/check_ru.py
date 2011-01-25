#!/usr/bin/python
import os
from subprocess import Popen, PIPE, STDOUT
import time
import re

def get_ru_list(rg_name):
	ru_list = []
	cmd = 'fshascli -v ' + rg_name
	output = os.popen(cmd).readlines()
	for line in output:
		m = re.match(r'^RecoveryUnit\s*(\S*)', line)
		if m:
			ru_list.append(m.group(1))
	return ru_list

def get_ru_role(ru_name):
	role = None
	cmd = 'fshascli -s ' + ru_name
	output = os.popen(cmd).readlines()
	for line in output:
		m = re.match(r"role\((\S*)\)", line)
		if m:
			role = m.group(1)
	return role

def is_active_ru(ru_name):
	return "ACTIVE" == get_ru_role(ru_name)

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
#	print("start to check RU " + ru_name + " ...")
	cmd = 'fshascli -s ' + ru_name
	output = os.popen(cmd).readlines()
	status, error_info = check_result(build_correct_ru_result(ru_name), output)
	if status:
		print("%-40s OK"%(ru_name))
	else:
		print("%-40s NOK:"%(ru_name))
		print(error_info)
	return status

def check_ru_status(ru_list):
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
			status = check_ru_status(ru_list)
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
#	print (r_list)
	if 'yes' in r_list and 'ok' in r_list:
		print("Clock is ok")
		return True
	else:
		print("Clock not ok!")
		return False

#	ret = p.communicate()[0]	
	
def get_node_list():
	node_list = []
	cmd = 'hwcli -o off'
	i = 0
	output = os.popen(cmd).readlines()
	for line in output:
		p = re.compile(r'(TCU-\d|CLA-\d|TDM\S*)\W+\w*\W*(\w*)\W*')
		m = p.search(line)
		if m and m.group(2) == "available":
			node_list.append(m.group(1))
	return node_list

def check_needed_node(node_list):
	num_tcu = 0
	num_tdm = 0
	num_cla = 0
	for node in node_list:
		if node.startswith("TCU"):
			num_tcu += 1
		if node.startswith("TDM"):
			num_tdm += 1
		if node.startswith("CLA"):
			num_cla += 1
	if num_tcu == 0:
		print "No Working DSP available"
	if num_tdm == 0:
		print "No Working TDM available"
	if num_cla == 0:
		print "No Working CLA available"
	return num_tcu and num_cla and num_tdm
	
def check_all():
	node_list = get_node_list()	
	if not check_needed_node(node_list):
		print "Please first make the node working!"
		return
	for node in node_list:
		if not check_rg_status("/"+node):
			ru_result = False


if __name__ == '__main__':
	if check_all():
		print("All Check is ok")
	else:
		print("Not all check passed, please first check the RU and clock status")
