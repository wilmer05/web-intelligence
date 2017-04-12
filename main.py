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
    first_file = sys.argv[1]
    last_file = sys.argv[2]
    q = None
    try:
        first_file = last_queue.last_id
        q = last_queue.q
    except:
        print "No problems."
	
    for x in range(int(first_file), int(last_file)):
        f = open("out", "a")
	try:
    		if len(sys.argv) >=4:
			ff = open("timeouts/" + str(x) + ".txt")
			lines = [line.rstrip('\n') for line in ff]
			ff.close()
			q = util.Queue()
			for line in lines:
				q.enqueue((line,1))				
			print "Readed timeouts queue."	
			
	except:
		print "Exception reading timeouts queue"
        file_name = "logs/" + constants.log_name + str(x) + ".txt.gz"
        out_file = "graph/" + constants.log_name + str(x) + ".txt"
        urls = log_filter.get_filtered_lines(file_name, out_file)
        #print "Urls ready..."
	urls = list(set(urls[1:]))
	urls.reverse()
        bfs.bfs(urls, q, x, out_file)
        f.write("Ready %s.\n" % str(x))
        f.close()
        q = None

