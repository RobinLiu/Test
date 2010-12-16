'''
Created on 2010-11-30

@author: reliu
'''
import urllib.request
from urllib.error import URLError
from html.parser import HTMLParser
from html.parser import HTMLParseError
import re

path ="http://www.google.com/search?start=0&num=10&lr=en&client=google-csbe&output=xml_no_dtd&cx=002365954963989332961:5el2ixoc8_o&q="
department = "computer science of "

'''
http://www.google.com/search?
  start=0
  &num=10
  &q=red+sox
  &cr=countryCA
  &lr=lang_fr
  &client=google-csbe
  &output=xml_no_dtd
  &cx=00255077836266642015:u-scht7a-8i
'''
def is_edu_link(url, is_edu_end):
    if is_edu_end:
        pattern = r"^http://\S*\.edu/?$"
        prog = re.compile(pattern)
        result = prog.search(url)
        return result
    else:
        pattern = r"^http://\S*\.edu/?\S*"
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
    def __init__(self, is_edu_end=True):
        HTMLParser.__init__(self)
        self.flag = 0
        self.school_flag = 1
        self.faculty_flag = 1
        self.link = ""
        self.faculty_link = []
        self.school_link = []
        self.name = ""
        self.is_edu_end = is_edu_end
        self.aflag = 0
        
    def handle_starttag(self, tag, attrs):
        if self.flag == 1 and tag == 'a':
            self.aflag = 1
            for k, v in attrs:
                if k == 'href':
                    self.link =  v

            if self.school_flag and is_edu_link(self.link, self.is_edu_end):
                self.school_link.append(self.link)
#                print("Find school link : " + self.link)
                self.school_flag = 0
        else:
            self.aflag = 0
            
        if tag == "div" :
            if len(attrs) > 0 and attrs[0][1] == "ires":
                self.flag = 1
            
    def handle_endtag(self, tag):
        if self.aflag and self.flag == 1 and tag == "a":
            if (re.findall("^\b*faculty\b*$", self.name) \
            or re.findall("^\b*people\b*$", self.name)) \
            and is_edu_link(self.link, False):
#                print("Faculty link find: " + self.link + "| Data:" + self.name)
                self.faculty_link.append(self.link)
            else:
                if re.findall("faculty", self.name) or re.findall("people", self.name):
                    print("uuu---:"+ self.name +"-- link: " + self.link)
            print(self.name)
            self.aflag = 0
        self.name = ""
                
    def handle_data(self, data):
        if self.aflag and self.flag > 0:
            self.name += data
            self.name = self.name.lower()
'''
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
'''
def get_encoding(response):
    if len(response) <= 0:
        return "utf-8"
    if 'Content-Type' in response and len(response['Content-Type']) > 0:
        contenttype = response['Content-Type']
#        print("contenttype: " + contenttype)
        g = re.compile("charset=(\S*)").search(contenttype)
        if g:
#            print("find encoding: " + g.groups()[0])
            return g.groups()[0]
    return "utf-8"
            
def get_web_content(url):
    content = ""
    if len(url) <= 0:
        return content
    print(url)
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.12 (KHTML, like Gecko) Chrome/9.0.587.0 Safari/534.12')]
    content = ""
    try:
        response = opener.open(url, timeout = 30)
    except URLError:
        print("Open URL {} exception: {}".format(url, URLError))
    except IOError:
        print("Open URL exception: {}".format(IOError))
    else:
        response_info = dict(response.info())
        encoding = get_encoding(response_info)
        content = response.read().decode(encoding)
    return content


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


import httplib2
from httplib2 import HttpLib2ErrorWithResponse
from httplib2 import ProxyInfo
try:
    import socks
except ImportError:
    socks = None
httplib2.debuglevel = 1  
'''


#def get_web_content(url):
#    data = ""
#    if len(url) <= 0:
#        return ""
##    p = ProxyInfo(proxy_type=socks.PROXY_TYPE_HTTP, proxy_host='10.159.167.30', proxy_port=8080)
#    h = httplib2.Http('.cache', timeout = 3)
#    header={'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.12 (KHTML, like Gecko) Chrome/9.0.587.0 Safari/534.12'}
#    try:
#        response, content = h.request(url, headers = header)
#    except :
#        print("HttpLib2ErrorWithResponse.desc")
#        return data
##    except Exception:
##        print(Exception)
##        return data
#    print("----1")
#    print(response["content-type"])
#    print("----2")
#    try:
#        encoding = get_encoding(response)
#        data = content.decode(encoding)
#    except UnicodeError:
#        print("Data not utf-8 coded. try ")
##    print(response)
##    print(data)
#    return data    
            
def get_search_raw_result(school, department):
    key = urllib.parse.quote(department + " " + school)
    url = path+key
    return get_web_content(url)

from threading import Thread, Lock

g_mutex = Lock()
nbr_school = 0
nbr_faculty = 0
class GetSchoolLink(Thread):
    def __init__(self, rank, school):
        Thread.__init__(self)
        self.school = school
        self.rank = rank
    def run(self):
        global nbr_school, nbr_faculty
        content = get_search_raw_result(self.school, department)
        if len(content) > 0:
            myparser = SchoolLinkParser()
            try:
                myparser.feed(content)
            except HTMLParseError:
                print("get_dept_link error: {}" .format(HTMLParseError))
            else:
                g_mutex.acquire()
                print("School {} Rank {}, info:".format(self.school, self.rank))
                if len(myparser.school_link) > 0:
                    print("school_link {}".format(myparser.school_link))
                    nbr_school = nbr_school + 1
                else:
                    print("school {} link not found".format(self.school))
                    second_parse = SchoolLinkParser(False)
                    try:
#                        print(content)
                        second_parse.feed(content)
                    except:
                        print("parse error")
                    print("2 time school_link {}".format(second_parse.school_link))
                    if len(second_parse.school_link) > 0:
                        nbr_school = nbr_school + 1
                if len(myparser.faculty_link) > 0:
                    print("faculty_link {}".format(myparser.faculty_link))
                    nbr_faculty = nbr_faculty + 1
                else:
                    print("faculty link not found")
                g_mutex.release()
        
'''
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
'''
import time
def print_u_file():
    flist = []
    with open("../u.txt") as u_file:
        for a_line in u_file:
            u_pattern = re.compile(r'(\d+)(\D+)(\d.?\d?)')
            g = u_pattern.search(a_line).groups()
            if g:
                flink = GetSchoolLink(g[0], g[1])
                flist.append(flink)
                flink.start()
                time.sleep(1)
#                print(g[1])
#                link_pair = get_dept_link(g[1], department)
#                for name in link_pair:
#                    print(g[0] + g[1] + " :" + link_pair[name])
#                    w_file.write(g[0] + g[1] + " :" + link_pair[name] +'\n')
#                    flink = get_faculty_link(link_pair[name])
#                    w_file.write("\tPossible faculty link:\n")
#                    for link in flink:
#                        w_file.write("\t\t" + link + "\n")
    for link in flist:
        link.join()


#if __name__ == '__main__':
#    get_dept_link("MIT", department)
#    print_u_file()
#    print(get_search_raw_result("MIT", department))
#    URL = "http://www.google.com/search?start=0&num=10&q=computer+science+MIT&lr=en&client=google-csbe&output=xml_no_dtd&cx=002365954963989332961:5el2ixoc8_o"
#    print(get_web_content(URL))
    
    '''query = urllib.urlencode({'q' : 'damon cortesi'})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' \
      % (query)
    search_results = urllib.urlopen(url)
    json = simplejson.loads(search_results.read())
    results = json['responseData']['results']
    for i in results:
      print i['title'] + ": " + i['url'] '''
    
import json
import urllib.request, urllib.parse

def showsome(searchfor):
    query = urllib.parse.urlencode({'q': searchfor})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    search_response = urllib.request.urlopen(url)
    print(url)
    search_results = search_response.read().decode("utf8")
    results = json.loads(search_results)
    data = results['responseData']
    print('Total results: %s' % data['cursor']['estimatedResultCount'])
    hits = data['results']
    print('Top %d hits:' % len(hits))
    for h in hits: print('    ', h['titleNoFormatting'], h['url'])
    print('For more results, see %s' % data['cursor']['moreResultsUrl'])

showsome('faculty of computer science Harvad')
print("--------------Done--------------")
print("find {} schools and {} links".format(nbr_school, nbr_faculty))

