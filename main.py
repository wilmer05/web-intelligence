import gzip
import json
import requests
import downloader
import util
import constants
import bfs
import log_filter
import sys
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

if __name__ == "__main__":
    f = open("out", "a")
    for x in range(int(sys.argv[1]), 10):
        file_name = "logs/" + constants.log_name + str(x) + ".txt"
        out_file = "graph/" + constants.log_name + str(x) + ".txt"
        urls = log_filter.get_filtered_lines(file_name, out_file)
        #print "Urls ready..."
        bfs.bfs(urls[1:])
        f.write("Ready %s.\n" % str(x))

