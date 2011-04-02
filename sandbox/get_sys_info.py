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

def get_node_list():
	node_list = []
	cmd = "hwcli -e '^[^d]' -o off"
	i = 0
	output = os.popen(cmd).readlines()
	for line in output:
		p = re.compile(r'(CLA\S*|TCU\S*|TDM\S*)\W+\w*\W*(\w*)\W*')
		m = p.search(line)
		if m and m.group(2) == "available":
			node_list.append(m.group(1))
	return node_list

def get_spec_node_list(node_list, node_name):
	spec_node_list = []
	for node in node_list:
		if node.startswith(node_name):
			spec_node_list.append(node)
	return spec_node_list

def is_active_tcu(node_tcu):
	ru_list = get_ru_list("/"+node_tcu)
	for ru in ru_list:
		m = re.search(r"MGW_DSPM", ru)
		if m:
			return is_active_ru(ru)

def get_active_tcu(tcu_list):
	active_tcu_list = []
	for tcu in tcu_list:
		if is_active_tcu(tcu):
			print "TCU " + tcu + " is active"
			active_tcu_list.append(tcu)
		else:
			print "TCU " + tcu + " is inactive"
	return active_tcu_list
			
if __name__ == '__main__':
	node_list = get_node_list()
	print "Node list:" 
	print node_list
	tcu_list = get_spec_node_list(node_list, "TCU")
	print "TCU node list:"
	print tcu_list
	tdm_list = get_spec_node_list(node_list, "TDM")
	print "TDM node list:"
	print tdm_list
	active_tcu_list = get_active_tcu(tcu_list)
	print "active tcu node list:"
	print active_tcu_list
