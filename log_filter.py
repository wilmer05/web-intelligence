import constants
import sys
import gzip

def get_filtered_lines(in_file, out_file, print_graph = True):
    f1 = gzip.open(in_file)
    data = f1.read()
    ff = []
    if print_graph:
        f = open(out_file, "w")
    for line in data.splitlines():
        sl = line.split("\t")
        if len(sl) < 5:
            continue
        valid = True
        for invalid_filter in constants.forbidden_search_words:
            if invalid_filter in sl[1]:
                valid = False
                break
        valid = valid and "http" in sl[4]
        if valid:
            if print_graph:
                f.write(sl[1] + "   ->   " + sl[4] + "\n")
            ff.append(sl[4])
    if print_graph:
        f.close()
    f1.close()
    return ff

def get_queries(file_name):
    f1 = gzip.open(file_name)
    data = f1.read()
    ff = []
    for line in data.splitlines():
        sl = line.split("\t")
        if len(sl) < 5:
            continue
        valid = True
        for invalid_filter in constants.forbidden_search_words:
            if invalid_filter in sl[1]:
                valid = False
                break
        valid = valid and ("http" in sl[4] or "www" in sl[4] or ".com" in sl[4])
        if valid:
            ff.append(sl[1])
    
    return ff
    

if __name__ == "__main__":
    print get_filtered_lines(sys.argv[1], sys.argv[2])
