import gzip
import json
import requests
import downloader
import util
import constants
import bfs
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

if __name__ == "__main__":
    bfs.bfs(["https://www.yahoo.com/"])
