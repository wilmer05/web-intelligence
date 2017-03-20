import util
import constants
from downloader import download_page
import os
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib
import os
from HTMLParser import HTMLParser
import sys 

class MyHTMLParser(HTMLParser):
    def __init__(self, q):
        HTMLParser.__init__(self)
        self.urls = []
    def handle_starttag(self, tag, attr):
        if tag == "a":
            for x,y in attr:
                if x=="href":
                    if y is not None and len(y)>0 and y[0] == "h":
                        if y[-1] != "/":
                            y += "/"
                        self.urls.append(y)
http = httplib2.Http()
status, response = http.request('http://www.nytimes.com')

def get_links_from_file(url):
    file_name = convert_url(url)
    f = open(file_name)
    data = f.read()
    next_urls = []
    html = MyHTMLParser(next_urls)
    html.feed(data)
    f.close()
    return html.urls

def convert_url(file_name):
    file_name = file_name.split("//")[1]
    if file_name[-1] != "/":
        file_name += "/"
    file_name = file_name.replace(":", "-")
    file_name = file_name.replace("/", "_")
    file_name = "pages/" + file_name + ".txt"
    return file_name

def file_exist(url):
    file_name = convert_url(url)
    return os.path.isfile(file_name)

def bfs(initial_nodes):
    q = util.Queue()
    for url in initial_nodes:
        q.enqueue((url,0))
    print "Starting BFS..."
    #sys.stdout.flush()
    download_cnt = 0
    failed = 0
    while q.size() > 0 and download_cnt < constants.max_download:    
       (url, depth) = q.dequeue()
       if depth > constants.max_depth:
            break
       if not file_exist(url) and download_page(url) > 0:
            download_cnt += 1 
            try:
                links = get_links_from_file(url)
                for next_url in links:
                    if not file_exist(next_url):
                        q.enqueue((next_url, depth + 1))
            except:
              failed += 1  
       
    print "Downloaded %s documents." % download_cnt
    print "%s documents with erros." % failed

if __name__ == "__main__":
    urls = ["https://www.yahoo.com/"] 
    bfs(urls)
