
def get_covered_by(doc, edges):
    cov = list()
    for u,v in edges:
        if u == doc:
            cov.append(v)
    return cov

def greedy_pick(edges, vis_left, vis_right):
    cnt = dict()
    best = -1
    best_d = None
    for u,v in edges:
        if u in vis_left:
            continue
        if v in vis_right:
            continue

        if u not in cnt:
            cnt[u] = 0
        cnt[u] += 1
        tmp = cnt[u]
        if tmp > best:
            best = tmp
            best_d = u
            
    return best_d, get_covered_by(best_d, edges)

    

