import constants
import numpy as np
from threading import Thread 
def multicore_compute_edges(tf, qtfidf, index):
    ln = len(qtfidf) // constants.NUMBER_OF_THREADS
    #print ln
    print "Each file will contain %s query_files edges" % str(ln)
    print "Computing edges"
    threads = []

    for i in range(0, constants.NUMBER_OF_THREADS):
        th = Thread(target = compute_edges, args = [tf, qtfidf[ln * i : ln*(i+1)], index, i*ln])
        th.start()
        threads.append(th)
    rest = len(qtfidf) % constants.NUMBER_OF_THREADS
    
    th = Thread(target = compute_edges, args = [tf, qtfidf[-rest: ], index, len(qtfidf) - ln * constants.NUMBER_OF_THREADS])
    th.start()
    threads.append(th)

    for t in threads: 
        t.join()

    print "Saliendo del multicore compute edges idx"

def compute_edges(ts, qtfidf, index, start_at = 0):

    cc = -1
    f2 = open(constants.EDGES_FOLDER + str(start_at) + "_" + str(ts) + "_" + constants.EDGES_FILE, "w")
    for q in qtfidf:
        cc += 1
        folder = (cc + start_at) / constants.EDGES_SPLIT
        file_number = (cc + start_at) % constants.EDGES_SPLIT
        fname = constants.EDGES_FOLDER + str(folder) + "/" + str(file_number) + "-" + str(ts)
        f2.write(str(cc + start_at) + " " + fname + "\n")
        f = open(fname, "w")
        prt = False
        sims = index[q]
        imp = sims
        #print np.nonzero(sims)
        imp = np.nonzero(sims)[0]
        if len(imp) == 0:
            continue
        for d in imp:
            s =  sims[d]
            if ts > s:
               continue
            f.write(str(d) + "\n")

        f.close()
    f2.close()
