import constants
import numpy as np
def compute_edges(ts, qtfidf, index):

    print "Computing edges"
    cc = -1

    f2 = open(constants.EDGES_FILE, "w")
    f2.close()
    for q in qtfidf:
        cc += 1
        folder = cc / constants.EDGES_SPLIT
        file_number = cc % constants.EDGES_SPLIT
        fname = constants.EDGES_FOLDER + str(folder) + "/" + str(file_number)
        f2 = open(constants.EDGES_FILE, "a")
        f2.write(str(cc) + " " + fname + "\n")
        f = open(fname, "w")
        prt = False
        sims = index[q]
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
    print "Saliendo compute edges idx"
