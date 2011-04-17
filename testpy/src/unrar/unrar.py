'''
Created on 2011-3-23

@author: Robin
'''

import os, sys
from subprocess import call
import shlex, subprocess

def walktree(top):
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
#        cmdpath = os.path.join("D:/", 'Program Files')
#        cmdpath = os.path.join(cmdpath, "WinRAR")
#        cmdpath = os.path.join(cmdpath, "unrar.exe")
#        cmdpath = "\"" + cmdpath + "\""
#        print(cmdpath)
#        cmd = '"D:/Program Files/WinRAR/unrar.exe" x -ad -ac '
#        os.system(cmd)
        if pathname.endswith(".rar"):
            pathname = "\"" + pathname + "\""
            cmd = '"D:/Program Files/WinRAR/unrar.exe"  ' + pathname
#           print(pathname)
            print(cmd)
            p = subprocess.Popen(['"D:/Program Files/WinRAR/unrar.exe"', 'x -ad -ac -y', pathname])
#            os.system(cmd)
#            
            

#if __name__ == __main__

walktree('D:\classic music')     
        