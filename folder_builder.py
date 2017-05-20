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
