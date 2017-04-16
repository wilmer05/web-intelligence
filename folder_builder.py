import os
import constants
try:
    os.makedirs("descargas/")
except:
    pass

for i in range(0,constants.HASH_SIZE):
    try:
        os.makedirs("descargas/" + str(i) + "/")
    except:
        pass
