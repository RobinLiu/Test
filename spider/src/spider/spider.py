'''
Created on 2010-11-30

@author: reliu
'''
import urllib.request
from urllib.error import URLError
from html.parser import HTMLParser
from html.parser import HTMLParseError
import re

path ="http://www.google.com/search?sourceid=chrome&ie=UTF-8&q="
department = "computer science"

def is_edu_link(url):
    pattern = r"^http://\S*\.edu/?$"
    prog = re.compile(pattern)
    result = prog.search(url)
    return result

def is_valid_link(url):
    pattern = r"http://\S*\.\S*"
    prog = re.compile(pattern)
    result = prog.search(url)
    if not result:
        print("URL: " + url + " is not valid link")
    return result

def cat_link(head, tail):
    ph = re.compile(r"(\S*)/$")
    pt = re.compile(r"^/\S*")
    if ph.search(head) and pt.search(tail):
        g = ph.search(head).groups()
        url = g[0] + tail
    else:
        url = head + tail
    return url
    

class SchoolLinkParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = 0
        self.school_flag = 0
        self.faculty_flag = 0
        self.link = ""
        self.name = ""
        
    def handle_starttag(self, tag, attrs):
#        print("Encountered a {} start tag, attrs is {}".format(tag, attrs))
        if self.flag == 1 and tag == 'a':
#            print("link :{}".format(attrs[0][1]), end=" ")
            if  is_edu_link(attrs[0][1]):
                self.link = attrs[0][1]
                self.flag = 0
            
        if tag == "div" :
            if len(attrs) > 0 and attrs[0][1] == "ires":
#                print("div {}".format(attrs))
                self.flag = 1
            
#    def handle_endtag(self, tag):
#        if self.flag == 1 and tag == "a":
##            print("Encountered a {} end tag".format(tag))
#            self.flag = 0
            
    def handle_data(self, data):
        if self.flag > 0:
#            print("handle data :{}".format(data))
            self.name += data

class FacultyLinkParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = 0
        self.link = []
        self.name = []
        self.tmplink =[]
            
    def handle_starttag(self, tag, attrs):
        if tag == "a" :
#            print("Encountered a {} start tag, attrs is {}".format(tag, attrs))
            if len(attrs) > 0 and re.findall("faculty", attrs[0][1]):
#                print("<< link is {}".format(attrs[0][1]))
                self.flag = 1
#                self.name, self.tmplink = attrs[0]

                for k, v in attrs:
                    if k=='href':
#                        print("v is :" + v)
                        self.tmplink.append(v)
#            print("link :{}".format(attrs[0][1]), end=" ")
                
    def handle_endtag(self, tag):
        if self.flag == 1 and tag == "a":
#            print(">>Encountered a end tag")
            self.flag = 0
            
    def handle_data(self, data):
        if self.flag == 1 and re.findall("(aculty)|(eople)", data):
#            print("Faculty=={}".format(data))
            print("Append {}".format(self.tmplink))
            self.link.extend(self.tmplink)
        else:
#            print("No use link {}".format(self.link))
            self.tmplink = []
            
'''def get_web_content(url):
    content = ""
    if len(url) <= 0:
        return content
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.12 (KHTML, like Gecko) Chrome/9.0.587.0 Safari/534.12')]
    content = ""
    try:
        content = opener.open(url).read().decode('utf-8')
    except URLError:
        print("opener.open exception: {}".format(URLError))
    except IOError:
        print("opener.open exception: {}".format(IOError))
    return content           
'''
'''
from http.client import HTTPConnection
HTTPConnection.debuglevel = 1
from urllib.request import urlopen

def get_web_content(url):
    content = ""
    if len(url) <= 0:
        return content
    response = urlopen(url)
    data = response.read().decode('utf-8')
    print(data)
    return data
'''

import httplib2
from httplib2 import HttpLib2ErrorWithResponse
httplib2.debuglevel = 1  

def get_encoding(response):
    if len(response) <= 0:
        return "utf-8"
    if 'content-type' in response and len(response['content-type']) > 0:
        contenttype = response['content-type']
        g = re.compile("charset=(\S*)").search(contenttype)
        if g:
            print("find encoding: " + g.groups()[0])
            return g.groups()[0]
    return "utf-8"

def get_web_content(url):
    data = ""
    if len(url) <= 0:
        return ""
    h = httplib2.Http('.cache', timeout = 3)
    header={'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.12 (KHTML, like Gecko) Chrome/9.0.587.0 Safari/534.12'}
    try:
        response, content = h.request(url, headers = header)
    except HttpLib2ErrorWithResponse:
        print(HttpLib2ErrorWithResponse.desc)
        return data
    except Exception:
        print(Exception)
        return data
    print("----1")
    print(response["content-type"])
    print("----2")
    try:
        encoding = get_encoding(response)
        data = content.decode(encoding)
    except UnicodeError:
        print("Data not utf-8 coded. try ")
#    print(response)
#    print(data)
    return data    
            
def get_search_raw_result(school, department):
    key = urllib.parse.quote(department + " " + school)
    url = path+key
    return get_web_content(url)

def get_dept_link(school, department):
    content = get_search_raw_result(school, department)
    if len(content) > 0:
        myparser = SchoolLinkParser()
        try:
            myparser.feed(content)
        except HTMLParseError:
            print("get_dept_link error: {}" .format(HTMLParseError))
            return {}
        return{myparser.name: myparser.link}
    return {}

def get_faculty_link(url):
    if not is_valid_link(url):
        return []
    flink = FacultyLinkParser()
    try:
        flink.feed(get_web_content(url))
    except HTMLParseError:
        print("get_faculty_link error: {}".format(HTMLParseError))
        return []
    
    tmplink = []
    for link in flink.link:
        if not is_valid_link(link):
            link = cat_link(url, link)
        tmplink.append(link)    
    flink.link = tmplink
    print("flink : {}".format(flink.link))
    return flink.link

def print_u_file():
    with open("../u.txt") as u_file:
        with open("../u1.txt", mode='w') as w_file:
            for a_line in u_file:
                u_pattern = re.compile(r'(\d+)(\D+)(\d.?\d?)')
                g = u_pattern.search(a_line).groups()
#                print(g[1])
                link_pair = get_dept_link(g[1], department)
                for name in link_pair:
                    print(g[0] + g[1] + " :" + link_pair[name])
                    w_file.write(g[0] + g[1] + " :" + link_pair[name] +'\n')
                    flink = get_faculty_link(link_pair[name])
                    w_file.write("\tPossible faculty link:\n")
                    for link in flink:
                        w_file.write("\t\t" + link + "\n")

class A:
    def __init__(self):
        self.str = "this is a"
    def __str__(self):
        return '<urlopen error %s>' % self.str
                            

if __name__ == '__main__':
    print_u_file()
    print("--------------Done--------------")
    


