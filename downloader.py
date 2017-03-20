import gzip
import json
import requests
import constants
import os.path
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

# Let's fetch the Common Crawl FAQ using the CC index
def build_url(url):
   url = url.replace("/", "%2F")
   url = url.replace(":", "%3A")
   return "http://index.commoncrawl.org/" + constants.index + "?url=" + url + "&output=json"

def download_page(url):
    if url[-1] != "/":
        url += "/"
    resp = requests.get(build_url(url))
    pages = [json.loads(x) for x in resp.content.strip().split('\n')]
    page = pages[0]

    if "error" in page:
        return 0

    prefix = 'https://commoncrawl.s3.amazonaws.com/'
    offset, length = int(page['offset']), int(page['length'])
    offset_end = offset + length - 1
    resp = requests.get(prefix + page['filename'], headers={'Range': 'bytes={}-{}'.format(offset, offset_end)})

    raw_data = StringIO(resp.content)
    f = gzip.GzipFile(fileobj=raw_data)

    data = f.read()
    file_name = url
    file_name = file_name.split("//")[1]
    file_name = file_name.replace(":", "-")
    file_name = file_name.replace("/", "_")
    file_name = "pages/" + file_name + ".txt"

    f2 = open(file_name, "w")
    f2.write(data)
    f2.close()    
    return len(data)

if __name__ == "__main__":
    download_page("http://yahoo.com")
