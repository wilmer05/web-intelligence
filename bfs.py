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
    if file_name is None:
        return []
    f = open(file_name)
    data = f.read()
    next_urls = []
    html = MyHTMLParser(next_urls)
    html.feed(data)
    f.close()
    return html.urls

def convert_url(file_name):
    tmp = file_name.split("//")[0]
    file_name = file_name.split("//")[1]
    if file_name is None or len(file_name) == 0:
        return None
    if file_name[-1] != "/":
        file_name += "/"
    file_name = file_name.replace(":", "-")
    file_name = file_name.replace("/", "_")
    file_name = "pages/" + file_name + ".txt"
    return file_name

def file_exist(url):
    if len(url) ==0:
        return False
    file_name = convert_url(url)
    return (file_name is not None) and os.path.isfile(file_name)

def bfs(initial_nodes, last_queue, file_id, graph_file):
    q = util.Queue()
    if last_queue is not None:
        print "Using last queue for %s" % str(file_id)
        q.items = last_queue
    else:
        for url in initial_nodes:
            q.enqueue((url,0))
    print "Starting BFS for file %s..." % str(file_id)
    #sys.stdout.flush()
    download_cnt = 0
    existing_url = 0
    failed = 0
    timeout_cnt = 0
    while q.size() > 0 and download_cnt < constants.max_download:    
       (url, depth) = q.dequeue()
       if depth > constants.max_depth:
            break
       try:
            exist = file_exist(url)
            if download_page(url) > 0:
       #if not file_exist(url) and download_page(url) > 0:
                try:
                    links = get_links_from_file(url)
                    for next_url in links:
                        #if not file_exist(next_url):
                        f = open(graph_file, "a")
                        f.write(url + "   ->   " + next_url + "\n")
                        f.close()
                        q.enqueue((next_url, depth + 1))
                    if not exist:
                        download_cnt += 1 
                except:
                    failed += 1 
       except:
            timeout_cnt += 1
            print "Connection timeout."
            if timeout_cnt > constants.max_timeout:
                f = open("last_queue_%s.py" % str(file_id), "w")
                f.write("from collections import deque\n")
                f.write("q = %s\n" % str(q.items))
                f.write("last_id = %s\n" % str(file_id))
                f.close()
                break
       
    print "Downloaded %s documents." % download_cnt
    print "%s documents with erros." % failed

if __name__ == "__main__":
    urls = ["https://www.yahoo.com/"] 
    bfs(urls)
