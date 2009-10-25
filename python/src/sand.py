'''import urllib2
response = urllib2.urlopen('http://python.org/')
html = response.read()
print html'''

import re
import operator
import httplib
import HTMLParser
import urllib
import htmllib
from xml.dom import minidom

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
       
def print_list(L):
    print"------list begin---------"
    for k,v in L:
        print k, "\t" ,v
    print"------list end---------"     

def load_dict_from_file(file,dict):
    f = open(file)
    try:
        for line in f:
            k,v = line.split()
            dict[k] = int(v)
            '''print k,v'''
    finally:
        f.close()
    
    
                           
def add_to_dict(word,dict):
    if dict.has_key(word):
        '''print "repeat\t", word '''
        dict[word] += 1
    else:
        dict[word] = 1
        '''print "New word\t", word'''
    '''print_dict() '''     

def get_word_from_string(str,dict):
    p = re.compile('[a-zA-Z]+')
    m = p.findall(str)
    if m:
        for word in m:
            '''print "Word\t",word'''
            add_to_dict(word.lower(),dict)
           
def loadfile(file,dict): 
    f = open(file)
    try:
        for line in f:
            get_word_from_string(line,dict)
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

def save_list_to_file(file,L):
    f = open(file,'w')
    try:
        for key, v in L:
            str = "%s \t %s\n"%(key.ljust(20),v)
            f.writelines(str)
    finally:
        f.close()  
        
def sort_dict_to_list(dict):
    '''r = sorted(dict.items(),cmp= lambda x,y:-cmp(x,y),key = lambda d:d[1])'''
    r = sorted(dict.items(), key=operator.itemgetter(0))
    r = sorted(r, key=operator.itemgetter(1),reverse=True)
    return r


def multikeysort(items, columns):
    from operator import itemgetter
    comparers = [ ((itemgetter(col[1:].strip()), -1) if col.startswith('-') else (itemgetter(col.strip()), 1)) for col in columns]
    def sign(a, b):
        if   a < b:  return -1
        elif a > b:  return 1
        else:        return 0
    def comparer(left, right):
        for fn, mult in comparers:
            result = sign(fn(left), fn(right))
            if result:
                return mult * result
        else:
            return 0
    return sorted(items, cmp=comparer)

def wordlist():
    filename="c:/2.txt"
    word_dict={}
    load_dict_from_file("c:/1.txt",word_dict)
    loadfile(filename,word_dict)
    '''print word_dict.keys()
    print_dict(word_dict)
    print "--------after sort-----------"'''
    d = sort_dict_to_list(word_dict)
    '''print_list(d)'''
    save_list_to_file("c:/3.txt",d)
    print "done!"
    '''save_dict_to_file("c:/1.txt",word_dict)'''    

def is_english_word(str):   
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection("dict.cn")
    request_str = "/ws.php?utf8=ture&q=%s"%str
    conn.request("POST",request_str)
    r1 = conn.getresponse()
    #print r1.status, r1.reason
    data1 = r1.read()
    
    xmldoc = minidom.parseString(data1)
    #print xmldoc.toxml()
    root = xmldoc.documentElement
    node = root.getElementsByTagName('def')[0]
    trans = node.childNodes[0].data
    #print trans
    if trans == "Not Found":
        print "%s is not an Engilsh word"%str    
 

def get_content_from_web(url):
    sock = urllib.urlopen(url)
    htmlsrc = sock.read()
    sock.close()
 
 
if __name__ == "__main__":
    '''is_english_word("tttttt")'''
    #get_content_from_web("")




    

