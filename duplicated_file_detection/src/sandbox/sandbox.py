'''
Created on 2010-12-12

@author: reliu
'''
import os
import filecmp
from os.path import join, getsize

g_duplicate_files = []

'''size segment in M '''
g_size_segment = ['1', '2', '5', '10', '50', '100', '200', '300', '500']
g_file_list = []

def init_file_list(file_list):
    del file_list[:]
    for i in range(len(g_size_segment)):
        g_file_list.append({})
    print(file_list)
    

def get_list_index(file_size):
    max_size = int(g_size_segment[-1]) * 1024 * 1024
    min_size = int(g_size_segment[0]) * 1024 * 1024
    if(file_size < min_size):
        return 0
    if(file_size >= max_size):
        return len(g_size_segment) - 1
    for i in range(len(g_size_segment)):
        if file_size >= (int(g_size_segment[i]) * 1024 * 1024) \
        and file_size < (int(g_size_segment[i + 1]) * 1024 * 1024):
            return i+1

def wirte_duplicated_file_path(file_path1, file_path2, file_size):
    with open("c:/file_list.txt", 'a') as r_file:
        r_file.write(file_path1 + "\t\t" + file_path2 + "\t\t" + file_size + "\n")
        r_file.flush()

def add_file_to_list(file_list, file_path, file_name):
    file_size = getsize(file_path)
    list_index = get_list_index(file_size)
#    print(list_index)
    if list_index == 0:
        return
    for k, v in file_list[list_index].items():
        if v[0] == file_name or v[1] == file_size:
            try:
                if filecmp.cmp(file_path, k):
                    print("Duplicated files find! first at: " + k + " and then found at: " +file_path)
                    wirte_duplicated_file_path(k, file_path, get_human_readable_size(getsize(file_path)))
                    g_duplicate_files.append([file_path, get_human_readable_size(getsize(file_path))])
                    return
            except IOError as err:
                print("IOError: " + str(err))
    file_list[list_index][file_path] = [file_name, file_size]

SUFFIXES = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

def get_human_readable_size(size):
    for suffix in SUFFIXES:
        size /=1024
        if size < 1024:
            return '{0:.1f} {1}'.format(size, suffix)

def list_files(dir, file_list):    
    for root, dirs, files in os.walk(dir):
        for file_name in files:
            file_path = ''
            drv, left = os.path.split(root);
            if(file_name.startswith(".")) or left.startswith("."):
                print("hide files:", file_name)
            else:
                file_path = join(root, file_name)
                add_file_to_list(file_list, file_path, file_name)
            
def print_duplicate_files(file_list):
    for i in range(len(file_list)):
        print("File: " + file_list[i][0] + " Size: " + file_list[i][1] + " duplicated")

if __name__ == '__main__':
    init_file_list(g_file_list)
#    list_files('D:/test', g_file_list)
#    print_duplicate_files(g_duplicate_files)
    drivers = ["c:/", "d:/"]
    for driver in drivers:
        list_files(driver, g_file_list)
    print(g_duplicate_files)
        



#TODO: filter .svn folders