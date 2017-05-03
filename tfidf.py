from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint
import sys
import constants
import os
from log_filter import get_queries
import geom
import matplotlib.pyplot as plt

def keys_in_word(keys, word):
    for i in keys:
        if i in word:
            return True
    return False

def get_dict_from_docs(documents, queries):
    stoplist = set('for a of the and to in'.split())
    blacklist = set('css $( < > { } foter _ - class= bgcolor'.split())
    print "Processing texts"
    cnt = 0
    texts = []
    all_q = set()
    for q in queries:
        for w in q:
            all_q.add(w)
    for document in documents:
        text = []
        for word in ''.join(open(document, "r").readlines()).lower().split():
            if (word not in stoplist) and (not keys_in_word(blacklist, word)) and (unicode(word, errors='ignore') in all_q):
                text.append(unicode(word, errors='ignore'))
        if len(text) > 0:
            texts.append(text)
        cnt += 1
        if cnt % 1000 == 0:
            print "Processed %s docs." % str(cnt)
    print "Processing succeeded"
    sz1 = len(texts)
    texts += queries
    frequency = defaultdict(int)

    for text in texts:
        for token in text:
            frequency[token] += 1
            
    return frequency, texts, sz1

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
    for i in range(first, last):
        doc_name = "logs/user-ct-test-collection-0" + str(i) + ".txt.gz"
        tq = get_queries(doc_name)
        total += len(tq)
        for q in tq:
            qs +=  [[unicode(word, errors='ignore') for word in q.split()]]
        qs.sort()
        sz = len(qs)
        ans.append(qs[0])
        for i in range(1, sz):
            if qs[i] != qs[i-1]:
                ans.append(qs[i])
    print "Total number of different queries: %s" % str(len(ans))
    return ans, total

def make_corpus(first, last):
    docs = []
    for i in range(0,constants.HASH_SIZE):
        folder = './descargas/' + str(i)
        for f in os.listdir(folder):
            docs.append(folder + '/' + f)
    actual_doc_sz = len(docs)
    queries, actual_q_sz = get_queries_from(first, last)
    szq = len(queries)
    dic, docs, sz_d = get_dict_from_docs(docs, queries)
    c_docs = convert_multiple_docs(dic, docs)
    dictionary = corpora.Dictionary(c_docs)
    corpus = [dictionary.doc2bow(doc) for doc in c_docs]
    print "Number of nonempty docs: %s \n Number of nonempty queries: %s" % (sz_d, str(len(queries)))
    cq = corpus[sz_d :]
    cd = corpus[0: sz_d]
    print "cq %s" % str(len(cq))
    tfidf = models.TfidfModel(corpus)
    return cd, cq, tfidf, actual_doc_sz, actual_q_sz

def get_best_doc_idx(d, v, ts):

    idx = -1
    best = set()
    for i in range(0, len(d)):
        if i in v or len(d[i]) ==0:
            continue
        co = d[i]
        if len(co) > len(best):
            best = co
            idx = i
    if idx > -1:
        sz = len(d)
        for i in range(0, sz):
            d[i] = d[i].difference(best)
    return idx, best

def get_doc_coverage(dd, qs, t):
    ret = set()
    for j in range(0, len(qs)):
        if geom.get_cos(dd, qs[j]) >=t:
            ret.add(j)

    return ret

def get_dot_and_plot(cd, cq, tfidf, threshold, actual_doc_sz, actual_q_sz):
    number_of_thresholds = 10
    thresholds = []
    docs_per_thr = []
    cdtfidf = []
    cqtfidf = []

    print "Computing cdtfidf"
    for doc in cd:
        cdtfidf.append(tfidf[doc])
    for q in cq:
        cqtfidf.append(tfidf[q])
    query_sz = len(cq)
    docs_sz = len(cd)
    #for x in range(0,number_of_thresholds):
    if True:
        #threshold = ((x+1) * 1.0) * (0.05/number_of_thresholds)
        #threshold = 0.01
        print "Tsh #%s" % (str(threshold))
        fig = plt.figure(1)
        covered = set()
        used_docs = set()
        print "Computing docs_coverage"
        docs_coverage = [ get_doc_coverage(dd, cqtfidf, threshold) for dd in cdtfidf ]
        print "docs_coverage computed"
        px = []
        py = []
        cnt = 0
        while True:
            bd, cov_q = get_best_doc_idx(docs_coverage, used_docs, threshold)
            size_before = len(covered)
            if bd == -1 or cnt > 50:
                break
            query_p = (1.0 * len(covered)) / query_sz
            used_docs.add(bd)
            covered = covered.union(cov_q)
            px.append((1.0*len(used_docs))/docs_sz)
            py.append(query_p)
            cnt += 1
            print cnt
        thresholds.append(threshold)
        docs_per_thr.append(cnt)
        
        #plt.subplot(2,5,x+1)
        plt.plot(px, py, 'b--')
        plt.ylabel('Percentage of covered queries over   %s' % actual_q_sz)
        plt.xlabel('Percentage of documents used over   %s' % actual_doc_sz)
        plt.title('Threshold = %s' % str(threshold))
        fig.savefig('figures/latest.png')


if __name__ == '__main__':
    if os.path.isfile(constants.CORPUS_FILE):
        corpus = corpora.MmCorpus(constants.CORPUS_FILE)
        dsz = int(sys.argv[4])
        qsz = int(sys.argv[5])
        tfidf = models.TfidfModel.load(constants.MODEL_FILE)
        cd = corpus[0:dsz]
        cq = corpus[dsz:dsz+qsz]
        print "Corpus: %s Queries %s " % (str(len(cd)), str(len(cq)))
    else:
        cd, cq, tfidf, dsz, qsz = make_corpus(int(sys.argv[1]), int(sys.argv[2]))
        tfidf.save(constants.MODEL_FILE)
        corpora.MmCorpus.serialize(constants.CORPUS_FILE, cd + cq)
    get_dot_and_plot(cd,cq, tfidf, float(sys.argv[3]), dsz, qsz)
