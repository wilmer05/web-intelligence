from math import sqrt
def get_cos(v1, v2, n1):
    sz1 = len(v1)
    sz2 = len(v2)
    #print sz2
    idx1 = 0
    idx2 = 0
    dot = 0
    if len(v1) == 0 or len(v2) ==0:
        return -50000000000
    n2 = get_norm(v2)
    while( idx2 < sz2 ):
        look_for = v2[idx2][0]
        l = 0
        r = sz1-1

        while(l < r):
            mid = (l + r) / 2
            if v1[mid][0] < look_for:
                l = mid + 1
            else:
                r = mid

        if r >= 0 and v1[r][0]==look_for:
            dot += v1[r][1] * v2[idx2][1]

        idx2 += 1

    return (1.0*dot)/(n1 * n2)

def get_norm(v1):
    total = 0.0
    for i in v1:
        total += i[1] * i[1]
    return sqrt(total)
