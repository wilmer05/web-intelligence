import gzip
import json
import requests
import constants
import os.path
import os
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
import requests
from bs4 import BeautifulSoup as bs
import urllib2
import converter
# Let's fetch the Common Crawl FAQ using the CC index
def build_url(url):
   url = url.replace("/", "%2F")
   url = url.replace(":", "%3A")
   return "http://index.commoncrawl.org/" + constants.index + "?url=" + url + "&output=json"

def download_page(url, use_common_crawl=True):
    try:
        cnt =  download_from_cc(url)
        if cnt == 0:
            return direct_download(url)
        return cnt
    except:
        return direct_download(url)

def direct_download(url):
    dir_name, file_name = converter.convert_url(url)
    if file_name is None:
        return 0

    if os.path.isfile(file_name):
        return 1
    try:
        r = requests.get(url, timeout=constants.REQUEST_TIMEOUT, allow_redirects=False)
    except:
        print "Error descargando directo: %s" % url   
        return 0

    f2 = open(file_name, "w")
    f2.write(r.text.encode('ascii', 'ignore'))

    f2.close()    
    return len(r.text.encode('ascii', 'ignore'))

def download_from_cc(url):
    dir_name, file_name = converter.convert_url(url)

    if os.path.isfile(file_name):
        return 1
    try:
        resp = requests.get(build_url(url), timeout=constants.REQUEST_TIMEOUT, allow_redirects=False)
    except:
        return 0
    pages = [json.loads(x) for x in resp.content.strip().split('\n')]
    page = pages[0]

    if "error" in page:
        return 0

    prefix = 'https://commoncrawl.s3.amazonaws.com/'
    offset, length = int(page['offset']), int(page['length'])
    offset_end = offset + length - 1
    resp = requests.get(prefix + page['filename'], headers={'Range': 'bytes={}-{}'.format(offset, offset_end)}, timeout=constants.REQUEST_TIMEOUT, allow_redirects=False)

    raw_data = StringIO(resp.content)
    f = gzip.GzipFile(fileobj=raw_data)

    data = f.read()

    f2 = open(file_name, "w")
    f2.write(data)
    f2.close()    
    return len(data)

if __name__ == "__main__":
    download_page("http://yahoo.com")
