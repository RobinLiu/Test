#!/usr/bin/python
import check_ru 

print ("call check_all ")
if check_ru.check_all():
	print ("Start to create Link......")
	os.system('/root/sgwrm/restart_ru.sh')
else:
	print("Not all check passed, check it first!!!")