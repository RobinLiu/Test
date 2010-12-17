#!/usr/bin/python
import getpass
import telnetlib
HOST = 'TDMNIP-0'
try:
	tn = telnetlib.Telnet()
except IOError :
	print("err: ")
if tn:
	tn.set_debuglevel(10)
	try:
		tn.open(HOST, 2999)
		tn.read_until('%')
	except Error:
		print ("error")
	print("telnet ok")
else:
	print("telnet nok")
#tn.read_until("%")
print (tn.read_very_eager())


tn.write("TDMLIC\n")
tn.read_until('TDMLIC')
tn.write("disp_file\n")
tn.read_all()
tn.write("exit\n")
tn.write("exit\n")
#print(tn.read_all())