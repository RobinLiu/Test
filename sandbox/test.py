#!/usr/bin/python
import os
from subprocess import Popen, PIPE, STDOUT
import time
import re

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
			error_info = "    " + k + " should be " + status_dict[k] + " But is " + v
			ret = False
			return ret, error_info
	return ret, error_info

def check_mo_status(mo_name):
	mo_status = get_mo_status(mo_name)
	status, error_info = cmp_mo_status(mo_status)
	if status:
		print("%-40s OK"%(mo_name))
	else:
		print("%-40s NOK:"%(mo_name))
		print(error_info)
	return status

def check_active_mo_status(mo_name):
	mo_status = get_mo_status(mo_name)
	if 'role' in mo_status and mo_status['role'] != 'ACTIVE':
		print "Role is not active"
	else:
		print "Need to check"
		

	
if __name__ == '__main__':
	check_mo_status("/CLA-0/MGW_CMFU-0")
	check_mo_status("/CLA-1/MGW_CMFU-1")
	check_active_mo_status("/")