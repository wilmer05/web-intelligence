import gzip
import json
import requests
import downloader
import util
import constants
import bfs
import log_filter
import sys
import last_queue
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

if __name__ == "__main__":
	
    if len(sys.argv) < 2:
        print "Usage: python main2.py <log_name> < <input>"
        sys.exit(0)
    urls = []
    for url in sys.stdin:
        url = url[:-1]
        urls.append(url)
    out_file = "graph/" +  sys.argv[1] + ".txt"
    urls = list(set(urls))
    urls.reverse()
    q = None
    bfs.bfs(urls, q, sys.argv[1], out_file)

