import os
import filecmp
from os.path import join, getsize
import threading

SUFFIXES = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

def get_human_readable_size(size):
    for suffix in SUFFIXES:
        size /=1024
        if size < 1024:
            return '{0:.3f} {1}'.format(size, suffix)
        
class FolderTree:
    def __init__(self, path, p):
        self.path = path
        self.parent = p
        self.folder_size = 0
        self.children = []
        
    def add_child(self, child):
        self.children.append(child)
    
    def get_folder_size(self):
        files_size = 0
        for root, dirs, files in os.walk(self.path):
            files_size = sum(getsize(join(root, name)) for name in files)
            for dir in dirs:
                subdir = join(root, dir)
                self.parent = root
                subFT = FolderTree(subdir, root)
                self.add_child(subFT)
                files_size += subFT.get_folder_size()
            self.folder_size = files_size    
            return files_size

def print_one(FB):
    print(FB.path, ": ", get_human_readable_size(FB.folder_size))
    if(len(FB.children) > 0):
        for subfolder in FB.children:
            print("\t", subfolder.path, get_human_readable_size(subfolder.folder_size))

def print_folder(FB, level):
    print(FB.path, ": ", get_human_readable_size(FB.folder_size))
    level -= 1
    if(level <=0):
        return
    if(len(FB.children) > 0):
        for subfolder in FB.children:
            print("---",  end="")
            print_folder(subfolder, level)



class dir(object):
    def __init__(self):
        self.SPACE = ""
        self.list = []
    
    def getCount(self, url):
        files = os.listdir(url)
        count = 0;
        for file in files:
            myfile = url + "\\" + file
            if os.path.isfile(myfile):
                count = count + 1
        return count
    
    def getDirList(self, url):
        files = os.listdir(url)
        fileNum = self.getCount(url)
        tmpNum = 0
        for file in files:
            myfile = url + "\\" + file
            size = os.path.getsize(myfile)
            if os.path.isfile(myfile):
                tmpNum = tmpNum + 1
                if (tmpNum != fileNum):
                    self.list.append(str(self.SPACE) + "├─" + file + "\n")
                else:
                    self.list.append(str(self.SPACE) + "└─" + file + "\n")
            if os.path.isdir(myfile):
                self.list.append(str(self.SPACE) + "├─" + file + "\n")
                # change into sub directory
                self.SPACE = self.SPACE + "│  "
                self.getDirList(myfile)
                # if iterator of sub directory is finished, reduce "?
                self.SPACE = self.SPACE[:-4]
        return self.list
    
    def writeList(self, url):
        f = open(url, 'w')
        f.writelines(self.list)
        print ("ok")
        f.close()
        
if __name__ == '__main__':
    d = dir()
    d.getDirList("c:/python25") # input directory
    d.writeList("c:/1.txt") # write to file

import codecs

def mdcode( data, encoding='utf-8' ): 
    if isinstance(data, str): 
        return data.encode(encoding) 

    for c in ('utf-8', 'gbk', 'gb2312','gb18030','utf-16'): 
        try: 
            return data.decode(c).encode( encoding ) 
        except: 
            pass 
    raise 'Unknown charset' 

def getCharSet( data ): 
    maping = ['utf-8','gbk','gb2312','gb18030','utf-16'] 

    if isinstance(data, str): 
        return "unicode" 

    for i in maping: 
        try: 
            data.decode(i) 
            return i 
        except: 
            pass 
    return "Unknow" 
            
#if __name__ == '__main__':
#    ft = FolderTree("D:\\reliu\\Desktop\\tmp\\", None)
#    ft.get_folder_size()
#    print_folder(ft, 4)
    