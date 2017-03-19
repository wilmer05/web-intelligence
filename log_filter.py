import constants
import sys

def get_filtered_lines(data):
    ff = []
    f = open(sys.argv[2], "w")
    for line in data.splitlines():
        sl = line.split("\t")
        valid = True
        for invalid_filter in constants.forbidden_search_words:
            if invalid_filter in sl[1]:
                valid = False
                break

        if valid:
            f.write(sl[1] + "   ->   " + sl[4] + "\n")
            ff.append(sl[4])
    f.close()
    return ff
    

if __name__ == "__main__":
    f = open(sys.argv[1])
    get_filtered_lines(f.read())
    f.close()
