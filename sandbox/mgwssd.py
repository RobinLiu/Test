#!/usr/bin/python
#
# Date of last known commit:
# $Date: 2011-03-10 14:46:35 +0200 (to, 10 maalis 2011) $
#
# Revision of last known commit:
# $Revision: 189 $
#
# Author who made the last known commit:
# $Author: tokarppi $
#
# The full URL of this file in the repository.
# $HeadURL: https://svne1.access.nokiasiemensnetworks.com/isource/svnroot/viptools4u/mgwssd/mgwssd.py $

"""
  mgwssd.py [OPTION]

  Options:
    <none>                    Open UI menu

    -h, --help                Print help
    -b, --basic               Collect Basic data and create Zip
    -f, --full                Collect Full data and create Zip

    -z <filename>, --unzip <filename> Unzip collected data

  Examples:
    mgwssd.py         Opens UI menu

    mgwssd.py -h      Prints help
    mgwssd.py --basic Collects Basic data and creates Zip

    mgwssd.py -z Oulu_20110217-13.13.02.zip   Unzip files (Requires Python 2.6)

"""

import sys
import getopt
import os
import string
import re
#from time import sleep => sleep(10)
import subprocess
import shlex
import tarfile, zipfile
import platform
from datetime import *

#PUBLIC VARIABLES
#----------------
#-----------------USER EDITABLE PART STARTS HERE--------------------
#Dict of prbs, key like 'bc2prb' is case sensitive and is the same one used for grepping logs.
#Currently YOU MAY MANUALLY EDIT this set to suit Your purposes, use hashmark to disable some prb, example hcdprb below
prbs = {'htaprb': '5E4',
        #'hcdprb': '5FB', example of disabling some prb, both log and msg mon.
        'bc2prb': '5F1',
        'rm2prb': '4B4',
        'lemana': '744',
        'VmgwHan': '5EC',
        'IPConnMgr': 'A25',
        'TDMConnMgr': 'A23',
        'cilprb': '5FA',
        'uhaprb': '646',
        'umzpro': '63A',
        'mw1pro': '5EC',
        'mlpprb': '909',
        'mloprb': '6B0'
       }
size_of_msg_buffer = 0 #YOU MAY MANUALLY EDIT this value; 0 = disable manual buffer size, using monster default 1024kB
#-----------------USER EDITABLE PART ENDS HERE----------------------
revision = "$Revision: 189 $"
scriptURL = "$HeadURL: https://svne1.access.nokiasiemensnetworks.com/isource/svnroot/viptools4u/mgwssd/mgwssd.py $"
file_list = [] #file list for all produced files
pid_list = [] #pid list for all the monster processes
omu_addr_list = [] #phys addresses
cm_addr_list = [] #phys addresses
hclb_addr_list = [] #phys addresses
#sisu_addr_list = ('0x300','0x400','0x500','0x600') #phys addresses of all sisus
sisu_addr_list = [] #phys addresses of all sisus
scliu_addr_list = [] #phys addresses of all sisus

clusterId = ""
target_path = "/var/log/mgwssd/" #Common storage place where data is gathered (no problems with quota
log_path = "/var/log/" #The path where logs are fetched

menu_items = [0, "1. Basic Data Collection.",
              0, "2. Full Data Collection.",
              0, "3. Message Monitoring and logs (Basic Data Collected first)",
              0, "4. Use binary message monitoring"]

basicDataCmds = [# Command History
                "toFile cmd_history.txt",
                "fsclish -c 'history'",
                # SW Information
                "toFile sw.txt",
                "fsclish -c 'show sw-manage list'",
                "fsclish -c 'show sw-manage current all'",
                "rpm -qa",
                "toFile disk_space.txt",
                "vgs",
                "lvs",
                #"fsclish -c 'show sw-manage embedded-sw version fru-location...'"
                #"fsclish -c 'show sw-manage embedded-sw version node...'"
                #
                "toFile config.txt",
                "fsclish -c 'show functional-unit comp-addr-info'",
                "fsclish -c 'show functional-unit unit-info'",
                "fsclish -c 'show functional-unit unit-type-info'",
                "fsclish -c 'show functional-unit group-addr-info'",
                "fscmfcli -s /CLA-0",
                "fsclish -c 'show has summary managed-object /'",
                "fsclish -c 'show has state managed-object *'",
                #
                "toFile licence.txt",
                "fsclish -c 'show license all'",
                "fsclish -c 'show license feature-mgmt all'",
                "fsclish -c 'show license target-id'",
                #
                "toFile vmgw_data.txt",
                "fsclish -c 'show vmgw common'",
                "fsclish -c 'show vmgw mgw mod 0'",
                "fsclish -c 'show vmgw h248log vid 0-84'",
                # Alarms
                "toFile alarms.txt",
                "fsclish -c 'show alarm active'",
                "fsclish -c 'show alarm blocking-rule all'",
                # Element Info
                "toFile element_info.txt",
                "fsclish -c 'show license target-id'",
                "fsclish -c 'show sw-manage current all'",
                # IP Configuration data...Scripti voisi tsekata mita nodeja elementissa on ja ottaa ssh:n yli ipconfig komennot joka nodelta. TODO
                "toFile ip_config.txt",
                "ip route",
                "ip route show table all",
                "fsclish -c 'show routing node CLA-0 route'",
                "fsclish -c 'show routing node CLA-0 static-route config'",
                "fsclish -c 'show routing node CLA-1 route'",
                "fsclish -c 'show routing node CLA-1 static-route config'",
                "fsclish -c 'show networking address'",
                "fsclish -c 'show networking vlan'",
                "fsclish -c 'show networking bond'",
                # IPBR & IP CAC data
                #"toFile ipbr_ipcac.txt",
                "fsclish -c 'show mgw-ip-userplane route ipbr ipbrid default'",
                "fsclish -c 'show mgw-ip-userplane route association ipbrid default'",
                #"fsclish -c 'show mgw userplane ipbrid-set'",
                "fsclish -c 'show mgw-ip-userplane ipcac mgw'",
                "fsclish -c 'show mgw-ip-userplane ipcac common'",
                #Parameter files
                "toFile parameter_files.txt",
                #"fsclish -c 'show app-parameter configuration-parameter'", #here some probs!
                # MGW common parameters, parameter files (PRFILE, FIFILE) not used in ATCA.
                "toFile common_parameters.txt",
                #"fsclish -c 'show app-parameter configuration-parameter'",
                "fsclish -c 'show mgw userplane dsp-profile'",
                "fsclish -c 'show mgw userplane common'",
                "fsclish -c 'show troubleshooting common'",
                "fsclish -c 'show vmgw common'",
                "fsclish -c 'show mgw iwf common'",
                "fsclish -c 'show tdm common'",
                "fsclish -c 'show mgw license parameter all'",
                "fsclish -c 'show mgw-ip-userplane ipcac common'",
                # Traffic data
                "toFile traffic.txt",
                "fsclish -c 'show license feature-mgmt usage all'",
                "fsclish -c 'show troubleshooting user-plane all-context mode 1'"
                # Unit data removed as was duplicate with config.txt
                #
                # More toFile tag and commands can be added here!
                #
                ]


fullDataCmds = [# testcli moved from basic data as this last so long!
                "toFile config.txt",
                "fstestcli",
                # DSP usage, how about DSP statistics and other DSP SCLI commands?
                "toFile dsp_usage.txt",
                "fsclish -c 'show mgw userplane dsp-profile'",
                "fsclish -c 'show mgw userplane common'",
                "/opt/nokiasiemens/SS_MGWLegUtilities/bin/mgwsprmcli.sh -ty",
                "/opt/nokiasiemens/SS_MGWLegUtilities/bin/mgwsprmcli.sh -ti",
                "/opt/nokiasiemens/SS_MGWLegUtilities/bin/mgwsprmcli.sh -tca",
                "/opt/nokiasiemens/SS_MGWLegUtilities/bin/mgwsprmcli.sh -tct",
                "/opt/nokiasiemens/SS_MGWLegUtilities/bin/mgwsprmcli.sh -tl",
                # Equipment
                "toFile equipment.txt",
                "fsclish -c 'show mgw synchronization all'",
                "fsclish -c 'show hardware inventory list brief include-empty'",
                "fsclish -c 'show hardware inventory list detailed include-empty'",
                "fsclish -c 'show hardware state list'",
                # ET data
                "toFile et_stm_data.txt",
                "fsclish -c 'show tdm pdh et-configuration'",
                "fsclish -c 'show tdm pdh et-state'",
                "fsclish -c 'show tdm pdh et-supervision et-index 0-10751'",
                "fsclish -c 'show tdm pdh letgr'",
                "fsclish -c 'show tdm pdh letgr-state'",
                #Announcements and tones
                "toFile anno_tone.txt",
                "fsclish -c 'show announcement-and-tone tone'",
                "fsclish -c 'show announcement-and-tone language-tag'",
                "fsclish -c 'show announcement-and-tone dtmf'",
                "fsclish -c 'show announcement-and-tone announcement tcu'",
                "fsclish -c 'show announcement-and-tone announcement load fnbr 1-3999 ftyp vat'",
                "fsclish -c 'show announcement-and-tone announcement load fnbr 3-3999 ftyp vad'",
                "fsclish -c 'show announcement-and-tone announcement load fnbr 4001-11999 ftyp extvat'",
                "fsclish -c 'show announcement-and-tone announcement load fnbr 4000-19999 ftyp extvad'",
                # Measurement data
                "toFile meas_config.txt",
                "fsclish -c 'show stats m-type all'",
                "fsclish -c 'show stats m-job all'",
                "fsclish -c 'show stats obj-list all'",
                "fsclish -c 'show stats t-job all'",
                # POSIX data
                "toFile posix.txt",
                "ps -aef",
                # Routing data
                "toFile routing.txt",
                "fsclish -c 'show tdm circuitgroup all'",
                "fsclish -c 'show tdm ater'",
                "fsclish -c 'show tdm semipermanent-connection common'",
                "fsclish -c 'show nnsf'",
                # Signalling Network
                "toFile signalling_network.txt",
                "fsclish -c 'show signaling sccp concerned-point-code all'",
                "fsclish -c 'show signaling sccp concerned-subsystem all'",
                "fsclish -c 'show signaling sccp destination-point-code all'",
                "fsclish -c 'show signaling sccp limits'",
                "fsclish -c 'show signaling sccp own-point-code all'",
                "fsclish -c 'show signaling sccp subsystem all'",
                "fsclish -c 'show signaling link-config link-profile all'",
                "fsclish -c 'show signaling link-config timer-profile all'",
                "fsclish -c 'show signaling sctp-profile all'",
                "fsclish -c 'show signaling service-access-point all'",
                #below command freezes in VMWare!
                "fsclish -c 'show signaling ss7 association all'",
                "fsclish -c 'show signaling ss7 link all'",
                "fsclish -c 'show signaling ss7 linkset all'",
                "fsclish -c 'show signaling ss7 m3ua-limits'",
                "fsclish -c 'show signaling ss7 mtp3-limits'",
                "fsclish -c 'show signaling ss7 nif-mgw-to-slc all'",
                "fsclish -c 'show signaling ss7 nif-point-code all'",
                "fsclish -c 'show signaling ss7 nif-ran-point-code all'",
                "fsclish -c 'show signaling ss7 own-point-code all'",
                "fsclish -c 'show signaling ss7 remote-as all'",
                "fsclish -c 'show signaling ss7 route all'",
                # User data
                "toFile user_data.txt",
                "fsclish -c 'show user-management group'",
                "fsclish -c 'show user-management user'",
                "fsclish -c 'show user-management permission'",
                #FlexiPlatform symptom data (name agreed to be fp_ssd.txt)
                "fsclish -c 'save symptom-report name fp_ssd.txt'"
                #
                # More toFile tag and commands can be added here!
                #
                ]

#----------------

###############################################################################
#
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

###############################################################################
#CONVERTS '|' to '\n' plus adds one '\n' between logs
def log_to_readable(filu):
    writefile = open("filu.tmp", "w") #add sensible path if write error happens
    readfile = open(filu, "r")
    #define translation table
    inni = "|"
    outti = "\n"
    transsitaabeli = string.maketrans(inni,outti)

    for line in readfile:
        writefile.write(line.translate(transsitaabeli)+ "\n")

    readfile.close()
    writefile.close()
    os.remove(filu)
    os.rename("filu.tmp",filu)

    return

###########################################################################
#
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
            tagScriptInfoToFile(file_string, clusterId)
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

###########################################################################
def start_and_append_pid( stringi ):
    #echo $! is the key here, it echoes just started monster process_id
    ret_val = os.popen( stringi + "& echo $!" ).read()
    for line in ret_val.splitlines():
        pid_list.append(line)
    return

###########################################################################
#
def msg_mon(prbs, stamp, clusterId, target_folder,  binary=False):
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

    for addr in sisu_addr_list:
        file_string = target_folder + clusterId + "_" + stamp + "_" + "SISU_" + addr  + ".log"
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

    #All the SISUs
    file_string = target_folder + clusterId + "_" + stamp + "_all_families.log"
    file_list.append(file_string)
    cmd_string = "monster -f " + s1
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

###############################################################################
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
        myzip = zipfile.ZipFile(target_folder + stamp + ".zip", "w", zipfile.ZIP_DEFLATED)
        myzip.write(target_folder + stamp + ".tar", os.path.basename(stamp + ".tar"))
        myzip.close()
        print"\n-------------------------------------------------------------------------------"
        print "Created zip: " + target_folder + stamp + ".zip"
        print"\n-------------------------------------------------------------------------------"
        os.remove(target_folder + stamp + ".tar") #you do not need tar no longer
        remove_files()

    return

###############################################################################
def unzip(file_name):
    print"\n-------------------------------------------------------------------------------"
    try:
        myzip = zipfile.ZipFile(file_name, "r")
        myzip.extractall()
    except IOError:
        print"unzip():File", file_name, "not found!"
    except AttributeError:
        print "Failed, Unzipping requires Python version 2.6 or later. You are using", platform.python_version()
    except:
        print "unzip Error:", sys.exc_info()[0]

    return

###############################################################################
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

###############################################################################
#
def printMenu(menu_items, analyse_available):
    print"\n-------------------------------------------------------------------------------"
    print"\nWelcome to MGWSSD \n(c) NSN 2011 " + revision + "\n"
    print"Select action:\n"

    for item in range(0, len(menu_items), 2):
        if menu_items[item]:
            print"(X)  " , menu_items[item+1]
        else:
            print"( )  " , menu_items[item+1]

    print"\n     e. Execute."
    if analyse_available == 1:
        print"     a. Analyse collected data. (Data Collected)"
    else:
        print"     a. Analyse collected data. (Data NOT Collected)"
    print"     q. Quit."
    return

###############################################################################
#
def logical_xor(first, second):
    return int(first) ^ int(second)

###############################################################################
#
def getTimeStamp():
    result = datetime.today().isoformat()[0:-7].replace(":", ".").replace("-", "").replace("T", "-")
    return result

###############################################################################
#
def getClusterId():
    try:
        cluster_id = os.popen("cat /etc/cluster-id").read()
        cluster_id = cluster_id
    except:
        return ""

    return cluster_id

###############################################################################
#
def tagScriptInfoToFile(tfile, clusterId):
    file = open(tfile, 'a')
    file.write("This data is collected with MGWSSD revision: " + revision + "\n" + scriptURL + "\n" + "TargetID: " + clusterId + "\n")
    file.close()
    return


###############################################################################
#
def tagCmd(cmd, tfile=None):
    file = open(tfile, 'a')
    #file.write("\n\n" + "***Command Help here***" + "\n") this is not implemted now
    file.write("\n" + getTimeStamp() + "\n" + cmd + "\n")
    file.close()
    return



###############################################################################
#
def sendCmd(cmd, tfile):
    #this = ""
    #if file != None:
    tagCmd(cmd, tfile)
    #orig: cmd = cmd + ">>" + tfile
    cmd = cmd + "| tee -a " + tfile
    ret = os.popen(cmd).read()
    #print "\n\n" + ret + "\n\n"
    #for line in ret.splitlines():
        #this = this + line + "\n"
    return ret.splitlines()

###############################################################################
#
def collectData(cmd_list, idstring, clusterId, target_folder):
    """This function collects Data from MGW
       Basic Data includes following items:
       TBD
       """

    tfile = []
    splitted_line = []
    result_file_nbr = 0
    command_count = 0
    cur_command = 1

    #print collectBasicData.__doc__
    #kurkkaa due to progress indicator
    for (i, cmd) in enumerate( cmd_list ) :
        #print i, cmd
        if cmd.find("toFile ") == 0:
            result_file_nbr = result_file_nbr + 1
        else:
            command_count = command_count + 1

    print"\n-------------------------------------------------------------------------------"
    print idstring + "data collection started", getTimeStamp()
    t1 = datetime.utcnow()
    for (i, cmd) in enumerate( cmd_list ) :
        #print i, cmd
        if cmd.find("toFile ") == 0:
            tfile = shlex.split(cmd)
            file_list.append(target_folder + tfile[1]) #Add each file to file list for tar package
            print getTimeStamp() + " Gathering data to target file:%s " % (target_folder+tfile[1])
            tagScriptInfoToFile(target_folder + tfile[1], clusterId)
        else:
            ret = sendCmd(cmd, target_folder + tfile[1])  #ret can be parsed when needed
            #print ret
            #fgh Get functional units
            #UNIT_NAME         LOG_ADDR  PHYS_ADDR  STATE    REDUNDANCY  MO_NAME
            #OMU-0             0x4002    0x0200     WO-EX    2N          /CLA-0/MGW_OMUFU-0
            #CM-0              0x4005    0x0300     WO-EX    2N          /CLA-0/MGW_CMFU-0
            #SISU-0            0x4AAE    0x0000     WO-EX    2N*M        /CLA-0/MGW_SISUFU-0
            #HCLB-0            0x4ABF    0x0100     WO-EX    2N*M        /CLA-0/MGW_HCLBFU-0
            #SCLIU-0           0x4B52    0x0400     WO-EX    SN+         /CLA-0/MGW_SCLIUFU-0
            if cmd.find("show functional-unit unit-info") != -1:
                for line in ret:
                    splitted_line = shlex.split(line)
                    if len(splitted_line) == 6:
                        if splitted_line[3].find("WO-EX") != -1:
                            if splitted_line[0].find("OMU") != -1:
                                omu_addr_list.append(splitted_line[2])
                            elif splitted_line[0].find("CM") != -1:
                                cm_addr_list.append(splitted_line[2])
                            elif splitted_line[0].find("SISU") != -1:
                                #sisu_addr_list[:] = []  # empty default list
                                sisu_addr_list.append(splitted_line[2])
                                #print sisu_addr_list
                            elif splitted_line[0].find("HCLB") != -1:
                                hclb_addr_list.append(splitted_line[2])
                            elif splitted_line[0].find("SCLIU") != -1:
                                scliu_addr_list.append(splitted_line[2])
                            else:
                                #HEADER or not intersting UNIT
                                pass

            print "Command " + str(cur_command) + "/" + str(command_count)
            cur_command = cur_command + 1


    t2 = datetime.utcnow()
    td = t2 - t1
    print idstring + "data collected, duration (seconds): ", td.seconds

    return


###############################################################################
#
def garbageCollection( file_list ):
    #cleaning routine...

    for filu in file_list:
        filesize = 0
        try:
            filesize = os.path.getsize(filu)
            #tagged file header roughly 180-190 bytes. Remove all but execErrors.txt
            if((filesize <= 200) and (filu.find("execErrors.txt") == -1)):
                print "empty file removed: " + filu
                #remove also from list
                #del(file_list[filu]) #here type error ku skoopissa bugi?
                os.remove(filu)
        except OSError:
            print"garbageCollection():File", filu, "not found!"
        except:
            print "garbageCollection Error:", sys.exc_info()[0]

    return


###############################################################################
#
def analyseData():
    print"\n-------------------------------------------------------------------------------"

    print"Data analysis not available in this revision..."

    return

###############################################################################
#
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

###############################################################################
#
def printMonMenu():
    print"\n-------------------------------------------------------------------------------"
    print"\nMessage Monitoring is active:\n"
    print"Pid \tUnit \tMonitored Processes"
    pid_index = 0
    for unit in sisu_addr_list:
        print pid_list[pid_index], "\t", unit, "\t", prbs
        pid_index = pid_index + 1

    print"\n     r. Kill all monitoring processes"
    print"        and return to main menu."


###############################################################################
#
def msgMonMenu():

    printMonMenu()

    getch = _Getch()
    while True:
        selection = getch()
        if selection == 'r':
            for pid in pid_list:
                killMonProcess(pid)
            break
        else:
            print"\n-------------------------------------------------------------------------------"
            print"ERROR: \"" + selection + "\" is invalid Selection!"

        printMonMenu()

###############################################################################
#
def execute():


    fullt1 = datetime.utcnow()
    data_collected = 0

    stamp = getTimeStamp()
    clusterId = getClusterId()
    target_folder = target_path + stamp + "/"
    print"\n-------------------------------------------------------------------------------"
    print "Execution started with timestamp: " + stamp + " in target: " + clusterId

    #Check target folder existence and if necessary create it
    #own folder for all data gathering added!
    if os.path.exists(target_folder) == False:
       cmdtosend = "mkdir -p " + target_folder
       os.popen(cmdtosend)
       print"target folder created:" + target_folder

    #Re-direct stderr to specific file
    #fgh toistaiseksi ruutulle notta kaikki saadaan funkkaan!
    #execErrors = open(target_folder + 'execErrors.txt', 'w')
    #sys.stderr = execErrors
    file_list.append(target_folder + "execErrors.txt")

    if menu_items[0]: # 1. Basic Data Collection.
        menu_items[0] = 0
        data_collected = 1 # This should be moved to actual collect functions to return correctly if nothing was collected.
        collectData(basicDataCmds, "Basic", clusterId, target_folder)
        grep_logs(prbs, stamp, clusterId, target_folder)

    if menu_items[2]: # 2. Full Data Collection.
        menu_items[2] = 0
        data_collected = 1 # This should be moved to actual collect functions to return correctly if nothing was collected.
        collectData(basicDataCmds, "Basic", clusterId, target_folder)
        collectData(fullDataCmds, "Full", clusterId, target_folder)
        grep_logs(prbs, stamp, clusterId, target_folder)

    if menu_items[4]: # 3. Message Monitoring and logs
        menu_items[4] = 0
        data_collected = 1 # This should be moved to actual collect functions to return correctly if nothing was collected.
        collectData(basicDataCmds, "Basic", clusterId, target_folder)
        #Default for MGW R&D Functional Testing...empty syslog/debug
        os.popen(">/var/log/syslog;>/var/log/debug")
        msg_mon(prbs, stamp, clusterId, target_folder, bool(menu_items[6]))
        msgMonMenu()
        grep_logs(prbs, stamp, clusterId, target_folder)

    fullt2 = datetime.utcnow()
    fulltd = fullt2 - fullt1
    print "Collecting data done, duration (seconds): ", fulltd.seconds


    #clear empty files (size 0) after execution
    garbageCollection( file_list )

    tar_zip( stamp, target_folder )
    # Remove all files from the list
    file_list[:] = []

    #Check for problems...
    if os.path.exists(target_folder + "execErrors.txt") == True:
        print"Please check file 'execErrors.txt' as problem observed!"

    return data_collected

###############################################################################
#
def askSelection():

    analyse_available = 0

    printMenu(menu_items, analyse_available)
    getch = _Getch()

    while True:
        selection = getch()
        if selection == 'q':
            print"Bye!"
            break

        elif selection == '1':
            menu_items[0] = logical_xor(menu_items[0], 1)
            menu_items[2] = 0
            menu_items[4] = 0

        elif selection == '2':
            menu_items[0] = 0
            menu_items[2] = logical_xor(menu_items[2], 1)
            menu_items[4] = 0

        elif selection == '3':
            menu_items[0] = 0
            menu_items[2] = 0
            menu_items[4] = logical_xor(menu_items[4], 1)

        elif selection == '4':
            menu_items[6] = logical_xor(menu_items[6], 1)

        elif selection == 'a':
            if analyse_available:
                analyseData()
            else:
                print"\n-------------------------------------------------------------------------------"
                print"ERROR: Data not collected. Please collect data first."

        elif selection == 'e':
            analyse_available = execute()

        else:
            print"\n-------------------------------------------------------------------------------"
            print"ERROR: \"" + selection + "\" is invalid Selection!"

        printMenu(menu_items, analyse_available)


###############################################################################
#
def main():

    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hbfz", ["help", "basic", "full", "unzip"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    #print "optiot:", opts
    #print "argut:", args

    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)

        if o in ("-b", "--basic"):
            menu_items[0] = 1
            dummy = execute();
            sys.exit(0)

        if o in ("-f", "--full"):
            menu_items[2] = 1
            dummy = execute();
            sys.exit(0)

        if o in ("-z", "--unzip"):
            for arg in args:
              print "Unzipping file:", arg
              unzip(arg)
            sys.exit(0)

    askSelection()

###############################################################################
#
if __name__ == "__main__":
    main()
