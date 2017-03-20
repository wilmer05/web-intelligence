import constants
import sys

def get_filtered_lines(in_file, out_file):
    f1 = open(in_file)
    data = f1.read()
    ff = []
    f = open(out_file, "w")
    for line in data.splitlines():
        sl = line.split("\t")
        valid = True
        for invalid_filter in constants.forbidden_search_words:
            if invalid_filter in sl[1]:
                valid = False
                break
        valid = valid and "http" in sl[4]
        if valid:
            f.write(sl[1] + "   ->   " + sl[4] + "\n")
            ff.append(sl[4])
    f.close()
    f1.close()
    return ff
    

if __name__ == "__main__":
    print get_filtered_lines(sys.argv[1], sys.argv[2])
