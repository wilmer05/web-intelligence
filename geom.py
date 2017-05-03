from math import sqrt
def get_cos(v1, v2):
    sz1 = len(v1)
    sz2 = len(v2)
    idx1 = 0
    idx2 = 0
    dot = 0
    n1 = 0
    n2 = 0
    if len(v1) == 0 or len(v2) ==0:
        return -50000000000
    while( idx1 < sz1 and idx2 < sz2 ):
        if v1[idx1][0] < v2[idx2][0]:
            n1 += v1[idx1][1] * v1[idx1][1]
            idx1 += 1
        elif v1[idx1][0] > v2[idx2][0]:
            n2+=v2[idx2][1] * v2[idx2][1]
            idx2 += 1
        else:
            dot += v1[idx1][1] * v2[idx2][1]
            n1 += v1[idx1][1] * v1[idx1][1]
            n2+=v2[idx2][1] * v2[idx2][1]
            idx1 += 1
            idx2 += 1

    while idx1 < sz1:
        n1 += v1[idx1][1] * v1[idx1][1]
        idx1 += 1

    while idx2 < sz2:
        n2 += v2[idx2][1] * v2[idx2][1]
        idx2+=1
    n1 = sqrt(n1)
    n2 = sqrt(n2)
    return (1.0*dot)/(n1 * n2)
