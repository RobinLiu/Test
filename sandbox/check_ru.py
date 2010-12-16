#!/usr/bin/python
import os
from subprocess import Popen, PIPE, STDOUT
import time

ru_list = [
			'/TDMNIP-0/MGW_TDMMGUFU-0',
			'/TDMNIP-0/MGW_TDMSNIUPFU-0',
			'/CLA-0/MGW_CMFU-0',
			'/CLA-0/MGW_SISUFU-0',
			'/TCU-0/MGW_DSPMRU0-0',
			'/CLA-0/MGW_OMUFU-0',
			'/CLA-0/FSSGWNetMgrServer',
			'/CLA-0/FSSS7SGUServer'
]
rg_list = [
			'/MGW_CMRG',
			'/SGWNetMgr',
			'/SS7SGU',
			'/MGW_CMRG',
			'/MGW_OMURG',
			'/MGW_SISURG-0',
			'/TDMNIP-0',
			'/TCU-0',
			'/CLA-0'
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
		if correct_result[index] != output[index]:
			error_info ="Status should be: " + correct_result[index] +"But is "+ output[index]
			result = False
	return result, error_info
		

def check_ru_status(ru_name):
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

def check_rg_status(rg_name):
#	print("start to check RG " + rg_name + " ...")
	cmd = 'fshascli -s ' + rg_name
	output = os.popen(cmd).readlines()
	status = check_result(build_correct_result(rg_name), output)
	if status:
		print("%-40s OK"%(rg_name))
	else:
		print("%-40s NOK"%(rg_name))
	return status

def check_clock():
	p = Popen(["fsclish"], shell=True, stdin=PIPE, stdout=PIPE)
	time.sleep(1)
	p.stdin.write("show mgw synchronization inputreference\n")
	time.sleep(1)
	p.stdin.write("quit\n")
	ret = p.stdout.read()
	print(ret)
	if ret.find("set-0      -      yes     2    2         2        gen2     5    ok        clk3a     ok            ") == -1:
		print("Clock not ok!")
		return False
	else:
		print("Clock is ok")
		return True
#	ret = p.communicate()[0]	
	
	
def check_all():
	global ru_list
	global rg_list
	ru_result = True
	print("Start to check RG...")
	for rg in rg_list:
		if not check_rg_status(rg):
#			print("RG %s is not ok"%rg)
			ru_result = False
	print("Check RU done, next check RU. \nChecking RU...")
	for ru in ru_list:
		if not check_ru_status(ru):
#			print("RU %s is not ok"%ru)
			ru_result = False
	print("Start to check clock setting...")
	return (check_clock() and ru_result)



	
if check_all():
	print("All Check is ok")
else:
	print("Not all check passed, please first check the RU and clock status")
	


