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
import converter

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
#http = httplib2.Http()
#status, response = http.request('http://www.nytimes.com')

def get_links_from_file(url):
    dir_name, file_name = convert_url(url)
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
    return converter.convert_url(file_name)

def file_exist(url):
    if len(url) ==0:
        return False
    dir_name, file_name = convert_url(url)
    return (file_name is not None) and os.path.isfile(file_name)

def bfs(initial_nodes, last_queue, file_id, graph_file):
    q = util.Queue()
    if last_queue is not None:
        print "Using last queue for %s" % str(file_id)
        q = last_queue
    else:
        for url in initial_nodes:
            q.enqueue((url,0))
    print "Starting BFS for file %s..." % str(file_id)
    #sys.stdout.flush()
    download_cnt = 0
    existing_url = 0
    failed = 0
    timeout_cnt = 0
    f = open("timeouts/" + str(file_id) + ".txt", "a")
    while q.size() > 0 and download_cnt < constants.max_download:    
       (url, depth) = q.dequeue()
       if depth > constants.max_depth:
            break
       try:
            exist = file_exist(url)

            #if download_page(url) > 0 or download_page(url, False) > 0:
            #if download_page(url) > 0: 
            print "Descargando: %s" % url
            if download_page(url, False) > 0:
                sys.stdout.flush()
                try:
                    links = get_links_from_file(url)
                    for next_url in links:
                        #if not file_exist(next_url):
                        f2 = open(graph_file, "a")
                        f2.write(url + "   ->   " + next_url + "\n")
                        f2.close()
                        q.enqueue((next_url, depth + 1))
                    if not exist:
                        download_cnt += 1 
                except:
                    failed += 1 
       except:
            timeout_cnt += 1
            print "Connection timeout."
	    f.write(url + "\n")
       
    f.close()
    print "Downloaded %s documents." % download_cnt
    print "%s documents with erros." % failed

if __name__ == "__main__":
    urls = ["https://www.yahoo.com/"] 
    bfs(urls)
