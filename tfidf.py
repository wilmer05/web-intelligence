from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint
import sys
import constants
import os
from log_filter import get_queries
import geom
#import matplotlib.pyplot as plt
import MyCorpus
import DocIter
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
    cnt2 = 0
    texts = []
    all_q = set()
    for q in queries:
        for w in q:
            all_q.add(w)
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
        for word in ''.join(open(document, "r").readlines()).lower().split():
            if (word not in stoplist) and (not keys_in_word(blacklist, word)) and (unicode(word, errors='ignore') in all_q):
        #        text.append(unicode(word, errors='ignore'))
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
            if qs[i] != qs[i-1]:
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
    #dic, docs, sz_d = get_dict_from_docs(docs, queries)
    sz_d = get_dict_from_docs(docs, queries)
    #c_docs = convert_multiple_docs(dic,docs)
    #dictionary = corpora.Dictionary(c_docs)
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
    tfidf = models.TfidfModel(corpus)
    return cd, cq, tfidf, cnt_d, actual_q_sz

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

def get_dot_and_plot(cd, cq, tfidf, threshold, actual_doc_sz, actual_q_sz, cnts, real_q_sz):
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
        #fig = plt.figure(1)
        covered = set()
        used_docs = set()
        print "Computing docs_coverage"
        docs_coverage = [ get_doc_coverage(dd, cqtfidf, threshold) for dd in cdtfidf ]
        print "docs_coverage computed"
        px = []
        py = []
        px2 = []
        py2 = []
        cnt = 0
        actual_q_total = 0
        while True:
            bd, cov_q = get_best_doc_idx(docs_coverage, used_docs, threshold)
            size_before = len(covered)
            if bd == -1:
                break
            for z in covered:
                actual_q_total += cnts[z]
            actual_query_p =  (100.0 * actual_q_total) / real_q_sz
            query_p = (100.0 * len(covered)) / query_sz
            used_docs.add(bd)
            covered = covered.union(cov_q)
            px.append((100.0*len(used_docs))/docs_sz)
            py.append(query_p)
            px2.append((100.0*len(used_docs))/docs_sz)
            py2.append(actual_query_p)
            if query_p > 83:
                break
            cnt += 1
            print cnt
        thresholds.append(threshold)
        docs_per_thr.append(cnt)
        #print px
        #print px2
        #print py
        #print py2
        #plt.subplot(2,5,x+1)
        #plt.plot(px, py, 'b--')
        #plt.ylabel('Percentage of covered unique queries over   %s' % actual_q_sz)
        #plt.xlabel('Percentage of documents used over   %s' % actual_doc_sz)
        #plt.title('Threshold = %s' % str(threshold))
        #fig.savefig('figures/latest-unique.png')
        #plt.figure(2)
        #plt.plot(px2, py2, 'b--')
        #plt.ylabel('Percentage of covered queries over   %s' % real_q_sz)
        #plt.xlabel('Percentage of documents used over   %s' % actual_doc_sz)
        #plt.title('Threshold = %s' % str(threshold))
        #fig.savefig('figures/latest.png')
	print "Px %s \n Py %s" % (str(px), str(py))
	print "Px2 %s \n Py2 %s" % (str(px2), str(py2))

if __name__ == '__main__':
    queries, actual_q_sz, counters = get_queries_from(int(sys.argv[1]), int(sys.argv[2]))
    if os.path.isfile(constants.CORPUS_FILE):
	print "Reading corpus"
        corpus = corpora.MmCorpus(constants.CORPUS_FILE)
        dsz = int(sys.argv[4])
        qsz = int(sys.argv[5])
	print "Reading model"
        tfidf = models.TfidfModel.load(constants.MODEL_FILE)
	print "Model readed"
        cd = corpus[0:-qsz]
        cq = corpus[qsz:]
        print "Corpus: %s Queries %s " % (str(len(cd)), str(len(cq)))
    else:
        cd, cq, tfidf, dsz, qsz = make_corpus(queries, actual_q_sz)
        print "Total of %s documents" % str(dsz)
        tfidf.save(constants.MODEL_FILE)
        corpora.MmCorpus.serialize(constants.CORPUS_FILE, cd + cq)
    get_dot_and_plot(cd,cq, tfidf, float(sys.argv[3]), dsz, qsz, counters, actual_q_sz)
