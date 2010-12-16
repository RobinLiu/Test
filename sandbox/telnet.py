#!/usr/bin/python
import getpass
import telnetlib
HOST = 'TDMNIP-0'
tn = telnetlib.Telnet(HOST, 2999)
tn.read_until("%")
tn.write("TDMLIC\n")
tn.write("?")
tn.write("exit\n")
tn.write("exit\n")
print(tn.read_all())