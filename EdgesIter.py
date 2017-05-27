import constants
from os import listdir
from os.path import isfile, join
class EdgesIter(object):

    def __init__(self, th):
        self.th = th

    def __iter__(self):
        onlyFiles = [f for f in listdir(constants.EDGES_FOLDER) if isfile(join(constants.EDGES_FOLDER, f)) and str(self.th) in f]
        for f in onlyFiles:
            for l in open(constants.EDGES_FOLDER + f):
                info = l.split()
                f_name = info[1]
                query = info[0]
                for line in open(f_name):
                    yield (int(line[:-1]), int(query))
