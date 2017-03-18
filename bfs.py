import util
import constants
from downloader import download_page
import os

def file_exist(file_name):
    file_name = file_name.replace(":", "-")
    file_name = file_name.replace("/", "_")
    file_name = "pages/" + file_name + ".txt"
    return os.path.isfile(file_name)

def bfs(initial_nodes):
    q = util.Queue()
    for url in initial_nodes:
        q.enqueue(url)
    download_cnt = 0
    while q.size() > 0 and download_cnt < constants.max_download:    
       url = q.dequeue()
       if not file_exist(url) and download_page(url) > 0:
            download_cnt += 1 
       
    print "Downloaded %s documents." % download_cnt

if __name__ == "__main__":
    bfs(["https://www.yahoo.com/"])
