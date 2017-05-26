import os
import constants
try:
    os.makedirs("corp/")
except:
    pass

for i in range(0,constants.HASH_SIZE):
    try:
        os.makedirs("corp/" + str(i) + "/")
    except:
        pass

try:
    os.makedirs(constants.INDEX_QUERIES_PREFIX)
except:
    pass

try:
    os.makedirs(constants.INDEX_PREFIX)
except:
    pass

try:
    os.makedirs(constants.EDGES_FOLDER)
except:
    pass


for i in range(0,constants.NUMBER_OF_EDGES_FOLDER):
    try:
        os.makedirs(constants.EDGES_FOLDER + str(i) + "/")
    except:
        pass
