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
