from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint
import sys
import constants
import os
from log_filter import get_queries
import geom
import matplotlib.pyplot as plt
import MyCorpus
import DocIter
import numpy as np
import greedy_pick
import graph_builder
import EdgesIter
import time
def keys_in_word(keys, word):
    for i in keys:
        if i in word:
            return True
    return False

def process_word(w, b_list):
    for x in b_list:
        w.replace(str(x), " ")
    return w.split()

def get_dict_from_docs(documents, queries):
    stoplist = set(u'for a of the and to in'.split())
    blacklist = set(u'\" <html> </i> <i> css $( <p> </p> <a> </a> </div> <div> < > { } foter _ - class= bgcolor = <br <a <li </li> </ul> <ul , '.split())
    print "Processing texts"
    cnt = 0
    cnt2 = 0
    texts = []
    all_q = set()
    for q in queries:
        for w in q:
            all_q.add(w.lower())
    mc = MyCorpus.MyCorpus()
    #frequency = defaultdict(int)
    for document in mc:
        cnt2+=1
        if cnt2 % 1000 == 0:
            print "Processed %s docs." % str(cnt2)
        #text = []
        #if cnt > 100:
        #    break
        counted = False
        if not os.path.isfile(document):
		    continue
        try:
            qyp = open((document + constants.PREFIX).replace('descargas', 'corp'), "w")
        except:
            continue
        for w in ''.join(open(document, "r").readlines()).lower().split():
            processed_word = process_word(w, blacklist)
            for word in processed_word:
#                if (word not in stoplist) and ( word not in blacklist) and (unicode(word, errors='ignore') in all_q):

                if word not in stoplist and (unicode(word, errors='ignore') in all_q):
            #        text.append(unicode(word, errors='ignore'))
                #    print word
                    if not counted:
                        cnt+=1
                        counted = True
                    #frequency[unicode(word, errors='ignore')] += 1
                    qyp.write(unicode(word, errors='ignore') + ' ')
        qyp.close()
         
        #if len(text) > 0:
        #    texts.append(text)
    print "Processing succeeded"
    #sz1 = len(texts)
    #texts += queries        
    #return frequency, texts, sz1
    return cnt

def convert_doc(frequency, doc):
    doc = [token for token in doc if frequency[token] > 1]
    return doc
    
def convert_multiple_docs(frequency, texts):
    docs = [convert_doc(frequency, text) for text in texts]
    return docs

def get_queries_from(first, last):
    qs = []
    ans = []
    total = 0
    counter = {}
    for i in range(first, last):
        doc_name = "logs/user-ct-test-collection-0" + str(i) + ".txt.gz"
        tq = get_queries(doc_name)
        total += len(tq)
        for q in tq:
            qs +=  [[unicode(word, errors='ignore') for word in q.split()]]
        qs.sort()
        sz = len(qs)
        ans.append(qs[0])
        counter[0] = 1
        cnt = 0
        for i in range(1, sz):
            #if qs[i] != qs[i-1]:
            if True:
                ans.append(qs[i])
                cnt += 1
                counter[cnt] = 0
            counter[cnt] += 1
    print "Total number of different queries: %s" % str(len(ans))
    return ans, total, counter

def get_words( x ):
    ccc = []
    ls = []
    try:
        ls = open(x).readlines()
    except:
        pass
    if len(ls) > 0:
        ccc = [ unicode(w, errors='ignore') for w in ls[0].split()]
    return ccc


def make_corpus(queries, actual_q_sz):
    docs = []
    for i in range(0,constants.HASH_SIZE):
        folder = './descargas/' + str(i)
        for f in os.listdir(folder):
            docs.append(folder + '/' + f)
    kq = open(constants.ALL_FILES, "w")
    for name in docs:
        if 'wil' not in name and 'txtW' not in name and name[-1] != 'w' and '\r' not in name:
            kq.write(name + "\n")
    kq.close()

    szq = len(queries)
    sz_d = get_dict_from_docs(docs, queries)
    di = DocIter.DocIter()
    dictionary = corpora.Dictionary()
    cnt_d = 0
    for x in di:
        cnt_d += 1
        ccc = get_words(x)
        if len (ccc) > 0:
            dictionary.add_documents([ccc])
    for qq in queries:
        dictionary.add_documents([qq])
    di = DocIter.DocIter()        
    corpus = [] 
    for x in di:
        ccc = get_words(x)
        if len (ccc) > 0:
           corpus.append(dictionary.doc2bow(get_words(x)))
    for qq in queries:
        corpus.append(dictionary.doc2bow(qq))
    print "Number of nonempty docs: %s \n Number of nonempty queries: %s" % (sz_d, str(len(queries)))
    #print "Corpus"
    #print len(corpus)
    #print sz_d
    cq = corpus[sz_d :]
    cd = corpus[0: sz_d]
    #print "cq %s" % str(len(cq))
    dictionary.save(constants.DICT_FILE)
    tfidf = models.TfidfModel(corpus)
    return cd, cq, tfidf, cnt_d, actual_q_sz, len(dictionary)

def get_edges(ts, qtfidf, index):

    edges = []
    print "Computing edges"
    cc = -1
    for q in qtfidf:
        cc += 1
        prt = False
        sims = index[q]
        imp = np.nonzero(sims)[0]
        if len(imp) == 0:
            continue
        for d in imp:
            s =  sims[d]
            if ts > s:
               continue
            edges.append((d, cc)) 

    print "Saliendo calc_edges idx"
    return edges



def get_best_doc_idx(dtfidf, corpus, covered, v, ts, qtfidf, index, index_q):

    ans = [-1 for t in ts]
    best = [set() for t in ts]
    cd = 0
    cnt = [{} for t in ts]
    cc = -1
    for q in qtfidf:
        cc += 1
        #print cc
        prt = False
        #print "Threshold %s" % (ts[i])
        sims = None
        imp = None
        for i in range(0,len(ts)):
            #print "Computing %s " % str(q) 
            if cc in covered[i]:
                continue
            if sims is None:
                sims = index[q]
                imp = np.nonzero(sims)[0]
            #if not prt and :
            if len(imp) == 0:
                continue
            #print len(imp) 
            #print imp
            for d in imp:
                s =  sims[d]
                if d in v[i]:
                    continue
                if ts[i] > s:
                   continue
                if d not in cnt[i]:
                   cnt[i][d] = 1
                else:
                   cnt[i][d] += 1

    for k in range(0, len(ts)):
        for d in cnt[k]:
            if ans[k] == -1 or cnt[k][d] > cnt[k][ans[k]]:
                ans[k] = d
    #print "ANS: %s " % str(ans)

    for k in range(0, len(ts)):
        if ans[k] != -1:
            sims = index_q[dtfidf[ans[k]]]
            for q, s in list(enumerate(sims)):
                if q not in covered and s >= ts[k]:
                    best[k].add(q)
    print "Saliendo best doc idx"
    return ans, best

def get_doc_coverage(dd, tfidf, qsz, t, corpus):
    ret = set()
    nd = geom.get_norm(tfidf[dd])
    for j in range(1,qsz+1):
        if geom.get_cos(dd, tfidf[corpus[-j]], nd) >=t:
            ret.add(j)

    return ret

def compute_greedy_and_plot(edges, used_docs, covered, cnts, real_q_sz, query_sz, docs_sz, q_p = 20, last_cov = 0, doc_sz_before = 0):
    px = []
    py = []
    cnt = 0
    t1 = time.time()
    while True:
        bd, cov_q = greedy_pick.greedy_pick(edges, used_docs, covered)
        if -1 == bd:
            break
        query_p = 0
        size_before = len(covered)
        actual_q_total = 0
        covered = covered.union(cov_q)
        for z in covered:
            actual_q_total += cnts[z]
        actual_query_p =  (100.0 * (actual_q_total - last_cov)) / real_q_sz
        query_p = (100.0 * len(covered)) / query_sz
        used_docs.add(bd)

        px.append((100.0* (len(used_docs) - doc_sz_before))/docs_sz)
        py.append(actual_query_p)
        cnt += 1
        print "Percentage of query covered %s" % str(query_p)
        if query_p > q_p:
            break
        t2 = time.time()
        if t2-t1 > constants.MAXTIME_COMPUTING:
            print "Max time reached"
            break
        print "Iteracion %s" % str(cnt)
        #print "Used docs: %s" % len(covered)
    return px, py, covered 

def get_dot_and_plot(corpus, q_corpus, tfidf, threshold, cnts, dic, index, index_q, edges_flag, computed_edges_flag, only_compute_edges_flag):
    number_of_thresholds = 10
    docs_per_thr = []
    print "Computing dtfidf"
    dtfidf = tfidf[corpus]
    qtfidf = tfidf[q_corpus]
    print "dtfidf computed"
    print "Tsh #%s" % (str(threshold))
    covered = set()
    used_docs = set()
    docs_coverage = []
    cc = 0
    px = []
    py = []
    #for q in dtfidf:
    #    print len(dtfidf)
    real_q_sz = len(qtfidf)
    query_sz = len(qtfidf)
    docs_sz = len(dtfidf)
    th2 = 0.3
    if not edges_flag:
        edges = get_edges(threshold, qtfidf, index)
    else:
        if not computed_edges_flag:
            print "### Computing edges ####"
            graph_builder.multicore_compute_edges(threshold, qtfidf, index)
            graph_builder.multicore_compute_edges(th2, qtfidf, index)
            #graph_builder.compute_edges(threshold, qtfidf, index)
            if only_compute_edges_flag:
                print "Edges computed, stoping script."
                return None

    edges = EdgesIter.EdgesIter(threshold)
    px, py, covered = compute_greedy_and_plot(edges, used_docs, covered, cnts, real_q_sz, query_sz, docs_sz)
    fig = plt.figure(1)
    plt.clf()

    plt.plot(px, py, '-', label='threshold %s' % str(threshold))
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.ylabel('Percentage of covered unique queries over   %s' % (real_q_sz))
    plt.xlabel('Percentage of documents used over   %s' % docs_sz)
    fig.savefig('figures/latest.png')

    edges = EdgesIter.EdgesIter(th2)
    px, py, covered = compute_greedy_and_plot(edges, used_docs, covered, cnts, real_q_sz, query_sz, docs_sz, 50, len(covered), len(used_docs))
    fig = plt.figure(1)
    plt.clf()

    plt.plot(px, py, '-', label='threshold %s' % th2)
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.ylabel('Percentage of covered unique queries over on tail  %s' % (real_q_sz))
    plt.xlabel('Percentage of documents used over   %s' % docs_sz)
    fig.savefig('figures/latest-tail.png')



if __name__ == '__main__':
    queries, actual_q_sz, counters = get_queries_from(int(sys.argv[1]), int(sys.argv[2]))
        
    if os.path.isfile(constants.CORPUS_FILE):
        print "Reading corpus"
        corpus = corpora.MmCorpus(constants.CORPUS_FILE)
        q_corpus = corpora.MmCorpus(constants.QUERIES_FILE)
        tfidf = models.TfidfModel.load(constants.MODEL_FILE)
        dic = corpora.Dictionary.load(constants.DICT_FILE)
        index = similarities.Similarity.load(constants.INDEX_FILE)
        index_q = similarities.Similarity.load(constants.INDEX_QUERIES_FILE)
        print "Corpus and models readed"
        print "Corpus: %s Queries %s " % (str(len(corpus)-len(q_corpus)), str(len(q_corpus)))
        
        get_dot_and_plot(corpus, q_corpus, tfidf, float(sys.argv[3]), counters, dic, index, index_q, constants.EDGES_FLAG in sys.argv, constants.EDGES_COMPUTED_FLAG in sys.argv, constants.ONLY_COMPUTE_EDGES_FLAG in sys.argv)
    else:
        cd, cq, tfidf, dsz, qsz, ldic = make_corpus(queries, actual_q_sz)
        print "Total of %s documents" % str(dsz)
        tfidf.save(constants.MODEL_FILE)
        corpora.MmCorpus.serialize(constants.CORPUS_FILE, cd)
        corpora.MmCorpus.serialize(constants.QUERIES_FILE, cq)
        print "LDIC = %s" % str(ldic)
        index = similarities.Similarity(constants.INDEX_PREFIX, tfidf[cd], ldic)
        index.save(constants.INDEX_FILE)
        index_q = similarities.Similarity(constants.INDEX_QUERIES_PREFIX, tfidf[cq], ldic)
        index_q.save(constants.INDEX_QUERIES_FILE)
