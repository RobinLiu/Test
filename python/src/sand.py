'''import urllib2
response = urllib2.urlopen('http://python.org/')
html = response.read()
print html'''

import re

'''def printdir(dir):
    file = os.listdir(dir)
    for name in file:
        fullpath = os.path.join(dir,name)
        if os.path.isdir(fullpath):
            printdir(fullpath)
        print fullpath'''
        
def print_dict(dict):
    print"------dict begin---------"
    for key in dict.keys():
        print key, "\t" ,dict[key]
    print"------dict end---------"    
                
def add_to_dict(word,dict):
    if dict.has_key(word):
        print "repeat\t", word 
        dict[word] += 1
    else:
        dict[word] = 1
        print "New word\t", word
    '''print_dict() '''     

def get_word_from_string(str,dict):
    p = re.compile('[a-zA-Z]+')
    m = p.findall(str)
    if m:
        for word in m:
            print "Word\t",word
            add_to_dict(word,dict)
           
def loadfile(file,dict): 
    f = open(file)
    try:
        for line in f:
            get_word_from_string(line,dict)
            print "dict len",len(dict)  
    finally:
        f.close()

def save_dict_to_file(file,dict):
    f = open(file,'w')
    try:
        for key in dict.keys():
            str = "%s \t %s\n"%(key.ljust(20),dict[key])
            f.writelines(str)
    finally:
        f.close()    

def sort_dict(dict):
    print sorted(dict.items(),key = lambda d:d[0])
                      
if __name__ == "__main__":
    filename="c:/2.txt"
    word_dict={"ttt":123}
    loadfile(filename,word_dict)
    print word_dict.keys()
    
    sort_dict(word_dict)
    print_dict(word_dict)
    '''save_dict_to_file("c:/3.txt",word_dict)'''
    print 

    

