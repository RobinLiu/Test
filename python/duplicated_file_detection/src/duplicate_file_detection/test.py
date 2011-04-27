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
        
#if __name__ == '__main__':
#    d = dir()
#    d.getDirList("c:/python25") # input directory
#    d.writeList("c:/1.txt") # write to file

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

def add_file_to_list(file_list, file_path):
    file_size = 0
    try:
        file_size = getsize(file_path)
    except Exception as err:
        print("Excetion while getsize:" + str(err))
    if file_size not in file_list:
        file_list[file_size]= [file_path];
    else:
        o_list = file_list[file_size]
        o_list.append(file_path)
        file_list[file_size]= o_list

def get_file_info(check_path, file_list):
    for root, dirs, files in os.walk(check_path):
        for dir in dirs:
            if(dir.startswith(".")):
                print("Ignore DIR: " + join(root, dir))
                dirs.remove(dir)
        for file in files:
            file_path = ''
            if(file.startswith(".")):
                print("hide files:", join(root, file))
            else:
                file_path = join(root, file)
                add_file_to_list(file_list, file_path)    

def print_suspect_dpfile(file_list):
    for file_size, files in file_list.items():
        if(len(files)>1) and cmp_in_list(files):
            print("%s"%(file_size))
            print("------------------------------------")
#            for file in files:
#                print("\t\t%s"%(file))
                

def cmp_file_name(path1, path2):
    head1, file1= os.path.split(path1)
    head2, file2= os.path.split(path2)
    return file1 == file2

def cmp_in_list(file_list):
    if(len(file_list)<=1):
        return None
    result = False
    l = len(file_list)
    j = 0
    i = 0
    
    while i <l:
        j = i+1
        while j < l:
#            print("i %s, j %s"%(i, j))
            if cmp_file_name(file_list[i], file_list[j]):
                print("\n%s\n%s\n"%(file_list[i], file_list[j]))
                result = True
            j = j + 1
        i = i + 1
                
    return result        
    
            
if __name__ == '__main__':
    check_path = "D:\\db\\Tech"
    file_list = {}
    get_file_info(check_path, file_list)
    print_suspect_dpfile(file_list)
#    print("size: %s"%os.path.getsize(check_path))
        
        
    