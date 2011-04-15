#!/usr/bin/python
import sys
import getopt
import os
import string
import re
import subprocess
import shlex
import tarfile, zipfile
import platform
from datetime import *

pid_list = []
file_list = []
size_of_msg_buffer = 0 #YOU MAY MANUALLY EDIT this value; 0 = disable manual buffer size, using monster default 1024kB
log_path = "/var/log/" #The path where logs are fetched
target_folder = '/var/tmp/'
prbs = {'srm':'a26',
        'lemana': '744',
        'uhaprb': '646'
       }


class _Getch:
    def __init__(self):
        self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def getTimeStamp():
    result = datetime.today().isoformat()[0:-7].replace(":", ".").replace("-", "").replace("T", "-")
    return result

def getClusterId():
    try:
        cluster_id = os.popen("cat /etc/cluster-id").read()
        cluster_id = cluster_id
    except:
        return ""

    return cluster_id
		
def tagCmd(cmd, tfile=None):
    file = open(tfile, 'a')
    #file.write("\n\n" + "***Command Help here***" + "\n") this is not implemted now
    file.write("\n" + getTimeStamp() + "\n" + cmd + "\n")
    file.close()
    return


def sendCmd(cmd, tfile):
    #this = ""
    #if file != None:
    tagCmd(cmd, tfile)
    #orig: cmd = cmd + ">>" + tfile
    cmd = cmd + "| tee -a " + tfile
    ret = os.popen(cmd).read()
    return ret.splitlines()
	
def getCMaddr():
	cmd = 'fsclish -c "show functional-unit unit-info"'
	ret = os.popen(cmd).read().splitlines();	
	for line in ret:
		m = re.match(r'CM-\d\s*(\S*)\s*(\S*)\s*WO-EX', line)
		if m:
			cm_addr_list = m.group(2)
#			print "CM phy addr is " + cm_addr_list
			return cm_addr_list
	return None

	
def killMonProcess(pid):
    #print"\n-------------------------------------------------------------------------------"
    #print "Killing process: ", str(pid)
    #check_pid = "ps -p" + str(pid)
    #result = os.popen(check_pid).read()
    #print result
    #for line in result.splitlines():
    #    if line.find(str(pid)) == 0:
    #        print"Process found."
    die_now = "kill -9 " + str(pid)
    os.popen(die_now)

    #print"Killed:", die_now

    return
    #print"NOTICE: Process " + str(pid) + " was not found. Propably dead already..."


def printMonMenu():
    print"\n-------------------------------------------------------------------------------"
    print"\nMessage Monitoring is active:\n"
    print"Pid \t\tUnit \tMonitored Processes"
    pid_index = 0
    print pid_list,"\t", "CM\t", prbs
#    for unit in sisu_addr_list:
#        print pid_list[pid_index], "\t", unit, "\t", prbs
#        pid_index = pid_index + 1

    print"\n     Press key 'f' to finish the log collection"


###########################################################################
def start_and_append_pid( stringi ):
    #echo $! is the key here, it echoes just started monster process_id
    ret_val = os.popen( stringi + "& echo $!" ).read()
    for line in ret_val.splitlines():
        pid_list.append(line)
    return

###########################################################################
#
def msg_mon(prbs, stamp, clusterId, target_folder, addr, binary=False):
    #TODO you may add ongoing monster check here plus possible warning, possible continue(y/n)
    print "Starting message monitoring..."
    s1 = ""
    for i in prbs.values():
        cmp_list = prbs.values() #need this to identify last value
        #do not write ',' to last item
        if i == cmp_list[len(prbs)-1]:
            s1 = s1 + i
        else:
            s1 = s1 + i + ","

#    for addr in sisu_addr_list:
#        file_string = target_folder + clusterId + "_" + stamp + "_" + "SISU_" + addr  + ".log"
#        file_list.append(file_string)
#        cmd_string = "monster -u " + addr + " -f " + s1
#        if size_of_msg_buffer > 0:
#            cmd_string = cmd_string + " -z " + str(size_of_msg_buffer)
#            #cmd_string = cmd_string + " -R -z " + str(size_of_msg_buffer)
#        if binary == True:
#            s = cmd_string + " -b " + file_string + " >tmp.txt"
#        else:
#            s = cmd_string + " > " + file_string
#        print s
#        z( s )

    #All the SISUs
    file_string = target_folder + clusterId + "_" + stamp + "_dmx_msg.log"
    file_list.append(file_string)
    cmd_string = "monster -u " + addr + " -f " + s1
    if size_of_msg_buffer > 0:
        cmd_string = cmd_string + " -z " + str(size_of_msg_buffer)
        #cmd_string = cmd_string + " -R -z " + str(size_of_msg_buffer)
    if binary == True:
        s = cmd_string + " -b " + file_string + " >tmp.txt"
    else:
        s = cmd_string + " > " + file_string
    print s
    start_and_append_pid( s )

    return


def msgMonMenu():
    printMonMenu()
    getch = _Getch()
    while True:
        selection = getch()
        if selection == 'f':
            for pid in pid_list:
                killMonProcess(pid)
            break
        else:
            print"\n-------------------------------------------------------------------------------"
            print"ERROR: \"" + selection + "\" is invalid Selection!"
        printMonMenu()


def grep_logs(prbs, stamp, clusterId, target_folder):
    print"\n-------------------------------------------------------------------------------"
    print "Gathering logs started..."

    #debug and syslog for each prb
    for i in list(prbs.keys()):
        filelist = ["debug","syslog"]
        for j in filelist:
            file_string = target_folder + i + "_" + j + ".txt"
            print file_string
            #tag common file header + changed to append >>
#            tagScriptInfoToFile(file_string, clusterId)
            file_list.append(file_string)
            s = "cat " + log_path + j + " |grep "+ i + ">>" + file_string
            os.system(s)
            #log_to_readable( file_string )

    #create complete logs zipfile
    filelist = ["master-syslog","syslog","debug","auth.log"]
    file_string = target_folder + "complete_logs.zip"
    myzip = zipfile.ZipFile(file_string, "w", zipfile.ZIP_DEFLATED)
    for i in filelist:
        try:
            myzip.write("/var/log/" + i, os.path.basename(i))
        except OSError:
            print"grep_logs():File", i, "not found!"
        except:
            print "grep_logs Error:", sys.exc_info()[0]
    myzip.close()
    print file_string
    file_list.append(file_string)

    #GATHER SPECIAL SYSLOG FILTERING PRODUCED LOGS AS SUCH!
    filelist = ["mdei.txt","tnsdl_runtime_crashes.txt"]
    for i in filelist:
        if os.path.exists(log_path + i) == True:
            cmdtosend = "cp " + log_path + i + " " + target_folder + i
            os.popen(cmdtosend)
            file_list.append(target_folder + i)
    return

def tar_zip(stamp, target_folder):
    print"\n-------------------------------------------------------------------------------"
    if len(file_list) == 0:
        print "0 files, .tar not created!"
    else:
        print"Starting to create zip file..."
        tar = tarfile.open(target_folder + stamp + ".tar", "w") #uncompressed format is fine for winzip
        for filu in file_list:
            #print filu
            try:
                tar.add(filu, os.path.basename(filu))
            except OSError:
                print"tar_zip():File", filu, "not found!"
            except:
                print "tar_zip Error:", sys.exc_info()[0]
        tar.close()
        file_name = target_folder + "SRM_log_" +stamp + ".zip"
        myzip = zipfile.ZipFile(file_name, "w", zipfile.ZIP_DEFLATED)
        myzip.write(target_folder + stamp + ".tar", os.path.basename(stamp + ".tar"))
        myzip.close()
        print"\n-------------------------------------------------------------------------------"
        print "Created zip: " + file_name
        print "Please send file :\"" + file_name + "\" to \"I_NWS_VIPT_RD_MGW_SGW_HZ@internal.nsn.com\""
        print"\n-------------------------------------------------------------------------------"
        os.remove(target_folder + stamp + ".tar") #you do not need tar no longer
        remove_files()
    return


def remove_files():
    if len(file_list) == 0:
        print "0 files to remove"
    else:
        for filu in file_list:
            try:
                os.remove(filu)
            except OSError:
                print"remove_files():File", filu, "not found!"
            except:
                print "remove_files Error:", sys.exc_info()[0]
    return

def main():
    stamp = getTimeStamp()
    clusterId = getClusterId()
    addr = getCMaddr()
    
    msg_mon(prbs, stamp, clusterId, target_folder, addr)
    msgMonMenu()
    grep_logs(prbs, stamp, clusterId, target_folder)
    tar_zip(stamp, target_folder)
	
if __name__ == '__main__':
    main()
