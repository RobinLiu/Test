'''
Created on 2010-11-30

@author: reliu
'''
import urllib.request
from html.parser import HTMLParser
import re

path ="http://www.google.com/search?sourceid=chrome&ie=UTF-8&q="
department = "computer science"

def is_edu_link(url):
    pattern = r"^http://\S*\.edu/?$"
    prog = re.compile(pattern)
    result = prog.search(url)
#    if not result:
#        print("URL: " + url + " is not edu ended link")
    return result

class SchoolLinkParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = 0
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
                href = [v for k, v in attrs if k=='href']
#                print("href {}".format(href))
                self.tmplink.extend(href)
                #self.link.extend
#            print("link :{}".format(attrs[0][1]), end=" ")
                
    def handle_endtag(self, tag):
        if self.flag == 1 and tag == "a":
#            print(">>Encountered a end tag")
            self.flag = 0
            
    def handle_data(self, data):
        if self.flag == 1 and re.findall("aculty", data):
#            print("Faculty=={}".format(data))
            self.link.extend(self.tmplink)
        else:
#            print("No use link {}".format(self.link))
            self.tmplink = []
            
def get_web_content(url):
    content = ""
    if len(url) <= 0:
        return content
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.12 (KHTML, like Gecko) Chrome/9.0.587.0 Safari/534.12')]
    content = ""
    try:
        content = opener.open(url).read().decode('utf-8')
    except Exception:
        print("opener.open exception")
#    else:
#        print("open url {} ok".format(url))
    return content           
            
def get_search_raw_result(school, department):
    key = urllib.parse.quote(department + " " + school)
    url = path+key
#    print(url)
    return get_web_content(url)

def get_dept_link(school, department):
    content = get_search_raw_result(school, department)
    if len(content) > 0:
        myparser = SchoolLinkParser()
        myparser.feed(content)
#        print("The link of \"{}\" is \"{}\"".format(myparser.name, myparser.link))
#        flink = FacultyLinkParser()
#        flink.feed(get_web_content(myparser.link))
#        print("flink : {}".format(flink.link))
        
        return{myparser.name: myparser.link}

def print_u_file():
    loop_count = 0
    with open("../u.txt") as u_file:
        with open("../u1.txt", mode='w') as w_file:
            for a_line in u_file:
#                if loop_count > 10:
#                    return
#                loop_count = loop_count + 1
                u_pattern = re.compile(r'(\d+)(\D+)(\d.?\d?)')
                g = u_pattern.search(a_line).groups()
#                print(g[1])
                link_pair = get_dept_link(g[1], department)
                for name in link_pair:
                    print(g[0] + g[1] + " :" + link_pair[name])
                    w_file.write(g[0] + g[1] + " :" + link_pair[name] +'\n')
#                    print("{} link: {}".format(g[1], link))
#                print("1-"+g[0] +"-2-"+ g.[1]+"-3-"  +'\n')
#                w_file.write(g[0] + g[1] +'\n')
#                print(g)
#                print(u_pattern.search(a_line).groups())
            


#def get_faulty_link():
if __name__ == '__main__':
#    get_dept_link("UIUC", department)
#    get_dept_link("MIT", department)
#    get_dept_link("UCLA", department)
    print_u_file()
#    is_edu_link("http://maps.google.com.hk/maps?um=1&ie=UTF-8&q=computer+science++Rutgers+Newark+(NJ)&fb=1&gl=hk&hq=computer+science&hnear=Rutgers,+Rutgers-Newark,+180+University+Ave,+Newark,+NJ+07102,+USA&cid=0,0,14656812902743094942&ei=bmb2TL-aKcGecIDT8MAE&sa=X&oi=local_result&ct=image&resnum=1&ved=0CBcQnwIwAA")
#    is_edu_link("http://www.marquette.edu/library/find/computer.shtml")
#    is_edu_link("http://euler.slu.edu/")
#    is_edu_link("http://euler.slu.edu")
#    is_edu_link("http://www.american.edu/cas/cs/index.cfm")
#    is_edu_link("")
#    is_edu_link("")
    print("--------------Done--------------")
    


