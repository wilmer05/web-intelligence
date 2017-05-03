import constants
class DocIter(object):
    def __iter__(self):
        for line in open(constants.ALL_FILES):
            yield line[:-1]  + constants.PREFIX
