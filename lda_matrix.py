from __future__ import division, print_function

import numpy as np
import itertools, io

from os import walk, path
import local as loc
import file_io as fi

from collections import OrderedDict, defaultdict

from handlers import HtmlHandler, TextHandler, TAGS
import sys
import lda
import entity_recognition as er

badwords = ['',]

#@profile
def vocab_from_file(raw_fpath, vocDict = dict(), vocab = [], intersect = True, interDict = dict(), isHTML = False):
    file_path = path.abspath(raw_fpath)
    #print('building vocabulary for file:')
    #print(file_path)     
    with io.open(file_path, 'rU', encoding='utf-8') as input:  
        if isHTML:

            #text = HtmlHandler(input.read()).text
            #text.filter_words(lambda (word,pos): pos in TAGS['NOUN'])

            raw_text = html_to_words(input.read())
            raw_text = unicode(raw_text, 'utf-8')
            text = TextHandler(raw_text)
            text = er.recognize_entities(text)
            #text.filter_words(lambda (word,pos): pos in TAGS['NOUN'])           
            
            keys = set(interDict.keys())

            for word in text:           
            #for word in text.words: 
                if word in vocDict: 
                    vocDict[word] += 1
                else:  
                    if not intersect or word in keys:
                        vocDict[word] = 1
                        vocab.append(word) 
        else:
            for word in itertools.chain.from_iterable(line.split() for line in input):
                if not intersect or word in interDict.values():
                    if word not in vocDict:
                        vocDict[word] = 1
                        vocab.append(word)
                    else:
                        vocDict[word] += 1
    return (vocDict, vocab)

#@profile
def build(files, extension ='htm', recurse = False, intersect = True, intersector_path = loc.intersector_path, interDict = dict()):                    
    vocDict = OrderedDict()
    vocab = []  
    if intersect:
        interDict = vocab_from_file(raw_fpath = intersector_path, intersect = False)[0]
    fileCount = 0
    dicList = []
    titles = ()
    for file in files:
        fdic, fvoc = vocab_from_file(raw_fpath = file, vocDict = OrderedDict(), vocab = vocab, intersect = intersect, interDict = interDict, isHTML = True)            
        #print("{0} <-> {1}".format(len(vocab), len(fvoc)))
        #vocab.extend(fvoc)
        titles += (file,)      
        keys = set(vocDict.keys())     
        for fword in fdic.keys():
            if fword not in keys:                
                vocDict[fword] = fdic[fword]
            else:
                vocDict[fword] += fdic[fword]
        #add to x
        dicList.append(fdic)                        
        fileCount += 1
    X = np.zeros((fileCount, len(vocDict)), dtype=int)  
    row_idx = 0
    vKeys = vocDict.keys();
    for dicti in dicList:
        for key in dicti.keys():
            col_idx = vKeys.index(key)            
            X[row_idx, col_idx] = dicti[key]
        row_idx += 1
    return (X, vocab, titles)

def fit(X, vocab, titles, num_topics=15):
    model = lda.LDA(n_topics=num_topics, n_iter=500, random_state=1)
    model.fit(X)
    doc_topic = model.doc_topic_
    topic_word = model.topic_word_
    #print("type(topic_word): {}".format(type(topic_word)))
    #print("shape: {}".format(topic_word.shape))
    n = 5 
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n+1):-1]
        print('*Topic {}\n- {}'.format(i, ' '.join(unicode(topic_words))))
    topic_files_dict = defaultdict(list)       
    numFiles = len(titles)       
    
    for n in range(numFiles):
        topic_most_pr = doc_topic[n].argmax()
        #print("{0} file most likely: {1}".format(n, topic_most_pr))
        #print("\t with: {0}", doc_topic[n][topic_most_pr])
        print('most probable topic is:' + str(topic_most_pr))
        topic_files_dict[topic_most_pr].append(titles[n])  
    
    for n in range(num_topics):
        print("topic {0} len: {1}".format(n, len(topic_files_dict[n])))
        if len(topic_files_dict[n]) > 1:
            n_X, n_vocab, titles = build(files=topic_files_dict[n],intersect=False)
            print("X: {0}, v: {1}".format(len(n_X), len(n_vocab)))
            if len(n_X) > 0 and len(n_vocab) > 0:
                if len(n_X) == len(X) and len(n_vocab) == len(vocab):
                    print("FOUND LEAF TOPIC FOR ARTICLES:")
                    print("TOPIC {0}".format(n))
                    for f in X:
                        print("\t{0}".format(f))
                else:
                    fit(n_X, n_vocab, titles)

if __name__ == "__main__":
    dir_path = loc.news_dir
    files = fi.getTopLevelFiles(dir_path)
    X, vocab, titles = build(files=files,intersect=False)
    fit(X, vocab, titles)
        
        