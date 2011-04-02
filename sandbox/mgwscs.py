#!/usr/bin/python
#
# Date of last known commit:
# $Date: 2011-02-18 17:48:57 +0800 (Fri, 18 Feb 2011) $
#
# Revision of last known commit:
# $Revision: 132 $
#
# Author who made the last known commit:
# $Author: tokarppi $
#
# The full URL of this file in the repository.
# $HeadURL: https://svne1.access.nokiasiemensnetworks.com/isource/svnroot/viptools4u/MGWSCS/mgwscs.py $

"""
  mgwssd.py [OPTION]

  Options:
    <none>                    Open UI menu

    -h, --help                Print help
    -b, --basic               Collect Basic data and create Zip
    -B, --basic-with-analysis Collect Basic data, analyse it and create Zip
    -f, --full                Collect Full data and create Zip
    -F, --full-with-analysis  Collect Full data, analyse it and create Zip

    -z <filename>, --unzip <filename> Unzip collected data

  Examples:
    mgwssd.py         Opens UI menu

    mgwssd.py -h      Prints help
    mgwssd.py --basic Collects Basic data and creates Zip
    mgwssd.py -F      Collects Full data, analyses data and creates Zip

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
#Transfer the script to default target folder /var/log/stdsymp/mgw and execute it from there
revision = "$Revision: 132 $"
scriptURL = "$HeadURL: https://svne1.access.nokiasiemensnetworks.com/isource/svnroot/viptools4u/MGWSCS/mgwscs.py $"
#Dict of prbs, key is the same one used for grepping logs
prbs = {'hta': '5E4', 'bc2': '5F1', 'rm2': '4B4', 'lemana': '744', 'VmgwHan': '5EC',
        'IPConnMgr': 'A25', 'cilprb': '5FA', 'uhaprb': '646', 'umzpro': '63A', 'mw1pro': '5EC'}
file_list = [] #file list for all produced files
pid_list = [] #pid list for all the monster processes
sisu_addr_list = ('0x300','0x400','0x500','0x600') #phys addresses of all sisus
#hclb_addr_list =
#cm_addr_list =
#omu_addr_list =
log_path = "/var/log/" #The path where logs are fetched

menu_items = [0, "1. Basic Data Collection.",
              0, "2. Full Data Collection.",
              0, "3. Basic Data Collection with message monitoring and logs.",
              0, "4. Full Data Collection with message monitoring and logs.",
              0, "5. Message Monitoring and logs",
              0, "6. Collect logs",
              0, "7. Message Monitoring",
              0, "8. Use binary message monitoring"]

basicDataCmds = [# Command History
                "toFile cmd_history.txt",
                "fsclish -c 'history'",
                # SW Information
                "toFile sw.txt",
                "fsclish -c 'show sw-manage list'",
                "fsclish -c 'show sw-manage current all'",
                "toFile disk_space.txt",
                "vgs",
                "lvs",
                #"fsclish -c 'show sw-manage embedded-sw version fru-location...'"
                #"fsclish -c 'show sw-manage embedded-sw version node...'"
                #
                "toFile config.txt",
                "fsclish -c 'show funit comp-addr-tbl all'",
                "fsclish -c 'show funit unit-info all'",
                "fsclish -c 'show funit unit-type all'",
                "fstestcli",
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
                "fsclish -c 'show troubleshooting user-plane all-context mode 1'",
                # Unit data
                "toFile unit_data.txt",
                "fsclish -c 'show funit unit-info all'",
                "fsclish -c 'show funit unit-type all'",
                "fsclish -c 'show funit comp-addr-tbl all'",
                "fsclish -c 'show funit grp-addr-tbl'",
                "fscmfcli -s /CLA-0"
                #
                # More toFile tag and commands can be added here!
                #
                ]


fullDataCmds = [# DSP usage, how about DSP statistics and other DSP SCLI commands?
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

###########################################################################
#
def grep_logs(prbs, stamp):
    print"\n-------------------------------------------------------------------------------"
    print "Gathering logs started..."

    #debug and syslog for each prb
    for i in list(prbs.keys()):
        file_string = stamp + "_" + i + "_debug" + ".txt"
        print file_string
        file_list.append(file_string)
        s = "cat " + log_path + "debug |grep "+ i +"|tr '|' '\n' > " + file_string
        os.system(s)
        file_string = stamp + "_" + i + "_syslog" + ".txt"
        print file_string
        file_list.append(file_string)
        s = "cat " + log_path + "syslog |grep "+ i +"|tr '|' '\n' > " + file_string
        os.system(s)

    #create complete logs zipfile
    filelist = ["master-syslog","syslog","debug","mdei.txt","tnsdl_runtime_crashes.txt","auth.log"]
    file_string = stamp+"_complete_logs.zip"
    myzip = zipfile.ZipFile(file_string, "w")
    for i in filelist:
        myzip.write("/var/log/" + i)
    myzip.close()
    print file_string
    file_list.append(file_string)
    #mdei.log: copy and make human readable --> ei loydy vmware
    #file_string = "mdei.txt"
    #print file_string
    #file_list.append(file_string)
    #s = "cat " + log_path + "mdei.log |tr '|' '\n' > " + file_string
    #os.system(s)

    #tnsdl_crash_log

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
def msg_mon(prbs, stamp, binary=False):
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
        file_string = stamp + "_" + "SISU_" + addr  + ".log"
        file_list.append(file_string)
        if binary == True:
            s = "monster -u " + addr + " -f " + s1 + " -b " + file_string + " >tmp.txt"
        else:
            s = "monster -u " + addr + " -f " + s1 + " > " + file_string
        start_and_append_pid( s )

    #All the SISUs
    file_string = stamp + "_all_families.log"
    file_list.append(file_string)
    if binary == True:
        s = "monster -f " + s1 + " -b " + file_string + " >tmp.txt"
    else:
        s = "monster -f " + s1 + " > " + file_string
    #bad_choice=(subprocess.Popen( s + "& echo $!", shell=True))
    start_and_append_pid( s )

    return

###############################################################################
def tar_zip(stamp):
    print"\n-------------------------------------------------------------------------------"
    if len(file_list) == 0:
        print "0 files, .tar not created!"
    else:
        print"Starting to create zip file..."

        #tar = tarfile.open(stamp+".tar", "w:gz")  #only linux understands this gzip tar format
        tar = tarfile.open(stamp+".tar", "w") #uncompressed format is fine for winzip
        for file in file_list:
            #print file
            tar.add(file)
        tar.close()
        myzip = zipfile.ZipFile(stamp+".zip", "w")
        myzip.write(stamp+".tar")
        myzip.close()
        print "Created zip: " + stamp + ".zip"
        os.remove(stamp+".tar") #you do not need tar no longer
        remove_files()

    return

###############################################################################
def unzip(file_name):
    print"\n-------------------------------------------------------------------------------"
    try:
        myzip = zipfile.ZipFile(file_name, "r")
        myzip.extractall()
    except IOError:
        print" File", file_name, "not found!"
    except AttributeError:
        print "Failed, Unzipping requires Python version 2.6 or later. You are using", platform.python_version()
    except:
        print "Error:", sys.exc_info()[0]

    return

###############################################################################
def remove_files():
    if len(file_list) == 0:
        print "0 files to remove"
    else:
        for file in file_list:
            os.remove(file)
    return

###############################################################################
#
def printMenu(menu_items, analyse_available):
    print"\n-------------------------------------------------------------------------------"
    print"\nWelcome to MGWSCS \n(c) NSN 2011 " + revision + "\n"
    print"Select action:\n"

    for item in range(0, len(menu_items), 2):
        if menu_items[item]:
            print"(X)  " , menu_items[item+1]
        else:
            print"( )  " , menu_items[item+1]

    print"\n     e. Execute."
    if analyse_available == 1:
        print"     a. Analyse collected data. (Data Collected)"
        print"     z. Zip and delete temporary files"
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
        cluster_id = cluster_id + "_"
    except:
        return ""
    return cluster_id

###############################################################################
#
def tagScriptInfoToFile(tfile):
    file = open(tfile, 'a')
    file.write("This data is collected with MGWSCS revision: " + revision + "\n" + scriptURL)
    file.close()
    return

###############################################################################
#
def tagCmdHelp(cmd, tfile=None):
    #file.write("\n\n" + "CommandHelpToHere")
    pass

###############################################################################
#
def tagCmd(cmd, tfile=None):
    file = open(tfile, 'a')
    file.write("\n\n" + "***Command Help here***" + "\n")
    file.write("\n" + getTimeStamp() + "\n" + cmd + "\n")
    file.close()
    return



###############################################################################
#
def sendCmd(cmd, tfile=None):
    this = ""
    if file != None:
        tagCmd(cmd, tfile)
        cmd = cmd + ">>" + tfile
    #HOX NEW: stderr &>> execErrors.txt stderr menee omaan defaltfileen, joka voidaan tarkastaa (size/content)
    ret = os.popen(cmd).read()
    #for line in ret.splitlines():
        #this = this + line + "\n"
    return ret.splitlines()

###############################################################################
#
def collectData(cmd_list, idstring):
    """This function collects Data from MGW
       Basic Data includes following items:
       TBD
       """

    tfile = []
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
            file_list.append(tfile[1]) #Add each file to file list for tar package
            print getTimeStamp() + " Gathering data to target file: %s " % tfile[1]
            tagScriptInfoToFile(tfile[1])
        else:
            ret = sendCmd(cmd, tfile[1])  #ret can be parsed when needed
            print "Command " + str(cur_command) + "/" + str(command_count)
            cur_command = cur_command + 1
    t2 = datetime.utcnow()
    td = t2 - t1
    print idstring + "data collected, duration (seconds): ", td.seconds
    #Check Execution errors from execErrors.txt

    return


###############################################################################
#
def garbageCollection():
    #cleaning routine...
    pass


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
def execute( stamp ):

    fullt1 = datetime.utcnow()
    data_collected = 0

    if menu_items[0]: # 1.
        menu_items[0] = 0
        data_collected = 1 # This should be moved to actual collect functions to return correctly if nothing was collected.
        collectData(basicDataCmds, "Basic")
        grep_logs(prbs, stamp)

    if menu_items[2]: # 2.
        menu_items[2] = 0
        data_collected = 1 # This should be moved to actual collect functions to return correctly if nothing was collected.
        collectData(basicDataCmds, "Basic")
        collectData(fullDataCmds, "Full")
        grep_logs(prbs, stamp)

    if menu_items[4]: # 3.
        menu_items[4] = 0
        data_collected = 1 # This should be moved to actual collect functions to return correctly if nothing was collected.
        collectData(basicDataCmds, "Basic")
        msg_mon(prbs, stamp,bool(menu_items[14]))
        msgMonMenu()
        grep_logs(prbs, stamp)

    if menu_items[6]: # 4.
        menu_items[6] = 0
        data_collected = 1 # This should be moved to actual collect functions to return correctly if nothing was collected.
        collectData(basicDataCmds, "Basic")
        collectData(fullDataCmds, "Full")
        msg_mon(prbs, stamp,bool(menu_items[14]))
        msgMonMenu()
        grep_logs(prbs, stamp)

    if menu_items[8]: # 5.
        menu_items[8] = 0
        data_collected = 1 # This should be moved to actual collect functions to return correctly if nothing was collected.
        msg_mon(prbs, stamp,bool(menu_items[14]))
        msgMonMenu()
        grep_logs(prbs, stamp)

    if menu_items[10]: # 6.
        menu_items[10] = 0
        data_collected = 1 # This should be moved to actual collect functions to return correctly if nothing was collected.
        grep_logs(prbs, stamp)

    if menu_items[12]: # 7.
        menu_items[12] = 0
        data_collected = 1 # This should be moved to actual collect functions to return correctly if nothing was collected.
        msg_mon(prbs, stamp,bool(menu_items[14]))
        msgMonMenu()


    fullt2 = datetime.utcnow()
    fulltd = fullt2 - fullt1
    print "Collecting data done, duration (seconds): ", fulltd.seconds

    return data_collected

###############################################################################
#
def askSelection(stamp):

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
            menu_items[6] = 0
            menu_items[8] = 0
            menu_items[10] = 0
            menu_items[12] = 0

        elif selection == '2':
            menu_items[0] = 0
            menu_items[2] = logical_xor(menu_items[2], 1)
            menu_items[4] = 0
            menu_items[6] = 0
            menu_items[8] = 0
            menu_items[10] = 0
            menu_items[12] = 0

        elif selection == '3':
            menu_items[0] = 0
            menu_items[2] = 0
            menu_items[4] = logical_xor(menu_items[4], 1)
            menu_items[6] = 0
            menu_items[8] = 0
            menu_items[10] = 0
            menu_items[12] = 0

        elif selection == '4':
            menu_items[0] = 0
            menu_items[2] = 0
            menu_items[4] = 0
            menu_items[6] = logical_xor(menu_items[6], 1)
            menu_items[8] = 0
            menu_items[10] = 0
            menu_items[12] = 0

        elif selection == '5':
            menu_items[0] = 0
            menu_items[2] = 0
            menu_items[4] = 0
            menu_items[6] = 0
            menu_items[8] = logical_xor(menu_items[8], 1)
            menu_items[10] = 0
            menu_items[12] = 0

        elif selection == '6':
            menu_items[0] = 0
            menu_items[2] = 0
            menu_items[4] = 0
            menu_items[6] = 0
            menu_items[8] = 0
            menu_items[10] = logical_xor(menu_items[10], 1)
            menu_items[12] = 0

        elif selection == '7':
            menu_items[0] = 0
            menu_items[2] = 0
            menu_items[4] = 0
            menu_items[6] = 0
            menu_items[8] = 0
            menu_items[10] = 0
            menu_items[12] = logical_xor(menu_items[12], 1)

        elif selection == '8':
            menu_items[14] = logical_xor(menu_items[14], 1)

        elif selection == 'a':
            if analyse_available:
                analyseData()
            else:
                print"\n-------------------------------------------------------------------------------"
                print"ERROR: Data not collected. Please collect data first."

        elif selection == 'e':
            stamp = getClusterId() + getTimeStamp()
            print"\n-------------------------------------------------------------------------------"
            print "Execution started with timestamp: " + stamp
            analyse_available = execute( stamp )

        elif selection == 'z':
            if analyse_available:
              tar_zip( stamp )
              analyse_available = 0
              # Remove all files from the list
              file_list[:] = []

        else:
            print"\n-------------------------------------------------------------------------------"
            print"ERROR: \"" + selection + "\" is invalid Selection!"

        printMenu(menu_items, analyse_available)

###############################################################################
#
def main():
    stamp = ""
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hbfBFz", ["help", "basic", "full", "basic-with-analysis", "full-with-analysis", "unzip"])
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
            stamp = getTimeStamp()
            collectData(basicDataCmds, "Basic")
            grep_logs(prbs, stamp)
            tar_zip( stamp )
            sys.exit(0)

        if o in ("-B", "--basic-with-analysis"):
            stamp = getTimeStamp()
            collectData(basicDataCmds, "Basic")
            grep_logs(prbs, stamp)
            analyseData()
            tar_zip( stamp )
            sys.exit(0)

        if o in ("-f", "--full"):
            stamp = getTimeStamp()
            collectData(basicDataCmds, "Basic")
            collectData(basicDataCmds, "Full")
            grep_logs(prbs, stamp)
            tar_zip( stamp )
            sys.exit(0)

        if o in ("-F", "--full-with-analysis"):
            stamp = getTimeStamp()
            collectData(basicDataCmds, "Basic")
            collectData(basicDataCmds, "Full")
            grep_logs(prbs, stamp)
            analyseData()
            tar_zip( stamp )
            sys.exit(0)

        if o in ("-z", "--unzip"):
          for arg in args:
            print "Unzipping file:", arg
            unzip(arg)
          sys.exit(0)

    askSelection(stamp)

###############################################################################
#
if __name__ == "__main__":
    main()
