import constants
class EdgesIter(object):
    def __iter__(self):
        for l in open(constants.EDGES_FILE):
            info = l.split()
            f_name = info[1]
            query = info[0]
            for line in open(f_name):
                yield (int(line[:-1]), int(query))
