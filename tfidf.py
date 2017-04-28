from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint
import sys
import constants
import os

def keys_in_word(keys, word):
    for i in keys:
        if i in word:
            return True
    return False

def get_dict_from_docs(documents):
    stoplist = set('for a of the and to in'.split())
    blacklist = set('< > { } foter _ - class='.split())
    texts = [[unicode(word, errors='ignore') for word in ''.join(open(document, "r").readlines()).lower().split() if word not in stoplist and not keys_in_word(blacklist, word)]
        for document in documents]
    frequency = defaultdict(int)

    for text in texts:
        for token in text:
            frequency[token] += 1
            
    return frequency, texts

def convert_doc(frequency, doc):
    doc = [token for token in doc if frequency[token] > 1]
    return doc
    
def convert_multiple_docs(frequency, texts):
    docs = [convert_doc(frequency, text) for text in texts]
    return docs

    
if __name__ == '__main__':
    docs = []
    for i in range(0,constants.HASH_SIZE):
        folder = './descargas/' + str(i)
        for f in os.listdir(folder):
            docs.append(folder + '/' + f)
    dic, docs = get_dict_from_docs(docs)
    c_docs = convert_multiple_docs(dic, docs)
    c_docs = [d for d in c_docs if len(d) > 0]
    #for doc in c_docs:
    #    if len(doc) == 0:
    #        print "BLA"
    #print c_docs
    dictionary = corpora.Dictionary(c_docs)
    #dictionary.save('/tmp/deerwester.dict')
    #print dictionary
    #print (dictionary.doc2bow(c_docs[0]))
    corpus = [dictionary.doc2bow(doc) for doc in c_docs]
    tfidf = models.TfidfModel(corpus)
    print tfidf[corpus[0]]


