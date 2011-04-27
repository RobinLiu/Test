'''
Created on 2011-04-23

@author: reliu
'''

import os
from os.path import join, getsize

SUFFIXES = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

def get_human_readable_size(size):
    for suffix in SUFFIXES:
        size /=1024
        if size < 1024:
            return '{0:.3f} {1}'.format(size, suffix)

class Folder:
    def __init__(self, path, parent):
        self.path = path
        self.parent = parent
        self.size = 0
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
        
class FolderTree:
    def __init__(self):
        self.root = None
        
    def insert(self, folder):
        if self.root is None:
            root = folder
        else:
            root.add_child(folder)
    
    def print_folder(self):
        if self.root is None:
            print("Empty folder tree")
            return
        iter = self.root.path
        print("%s"%iter.path)
        while(len(iter.childer) > 0):
            children_list = iter.children
        
            
        
    
#    def add_child(self, Folder, child):
#        Folder.add_child(child)
#    
#    def get_folder_size(self, folder):
#        files_size = 0
#        for root, dirs, files in os.walk(folder.path):
#            files_size = sum(getsize(join(root, name)) for name in files)
#            print("1")
#            for dir in dirs:
#                subdir = join(root, dir)
#                folder.parent = root
#                subfd = Folder(subdir)
#                folder.add_child(subfd)
#                files_size += subfd.get_folder_size(subfd)
#                print("size of %s is %s"%(root, files_size))
#        self.folder_size = files_size    
#        return files_size

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
            
if __name__ == '__main__':
    folder_path = 'D:\reliu\Desktop\backup'
    ft = FolderTree(folder_path)
    print("folder size is %s"%ft.get_folder_size())
    