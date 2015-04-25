from __future__ import division, print_function

import numpy as np
import itertools, io

from os import walk, path
import local as loc
import file_io as fi

from collections import OrderedDict, defaultdict
from text_manip import html_to_words
from handlers import HtmlHandler, TextHandler, TAGS
import sys
import lda
import multiprocessing
import entity_recognition as er
from joblib import Parallel, delayed

#@profile
def cross_reference_tokens():
    return 1
def probabilify(pdic):
    vals = pdic.values()
    wordCount = sum(vals)
    keys = pdic.iterkeys()
    for key in keys:
       pdic[key] /= float(wordCount) 
    return pdic
def vocab_from_file(raw_fpath, vocDict = dict(), intersect = True, interDict = dict(), isHTML = False, useEntities = False):
    fdic = dict()
    file_path = path.abspath(raw_fpath)
    print('building vocabulary for file:')
    print(file_path)
    with open('intersection_entity.txt', 'a+') as inf:
        inf.write('\nENTITIES IN FILE:')
        inf.write(file_path)
    with io.open(file_path, 'rU', encoding='utf-8') as input:  
        if isHTML:
            #text = HtmlHandler(input.read()).text
            #text.filter_words(lambda (word,pos): pos in TAGS['NOUN'])
            raw_text = html_to_words(input.read())
            raw_text = unicode(raw_text, 'utf-8')
            text = TextHandler(raw_text)
            if useEntities:
                words = er.recognize_entities(text.sentences, intersect=True, intersector=interDict)
            else:
                words = text.words                                   
            keys = set(interDict.keys())
            for word in words:           
            #for word in text.words: 
                if word in fdic: 
                    fdic[word] += 1
                else:  
                    if not intersect or word in keys:
                        fdic[word] = 1                        
        else:
            for word in itertools.chain.from_iterable(line.split() for line in input):
                if not intersect or word in interDict.values():
                    if word not in fdic:
                        fdic[word] = 1
                    else:
                        fdic[word] += 1
    return fdic

def vocabs_from_files(file, interDict, intersect=True, useEntities = False):
    return vocab_from_file(raw_fpath = file, vocDict = OrderedDict(), intersect = intersect, interDict = interDict, isHTML = True, useEntities = useEntities)               
           
#@profile
def build(files, extension ='htm', recurse = False, intersect = True, intersector_path = loc.intersector_path, interDict = dict()):                    
    vocDict = OrderedDict()
    vocab = []  
    if intersect:
        interDict = vocab_from_file(raw_fpath = intersector_path, intersect=False)
        interDict = probabilify(interDict)
    fileCount = 0
    dicList = []
    titles = ()
    for n in range(len(files)):
        titles += files[n],
    #num_cores = multiprocessing.cpu_count()
    #rets = Parallel(n_jobs=num_cores)(delayed(vocabs_from_files)(file, interDict, useEntities = True) for file in files)  
    rets = []
    for file in files:
        rets.append(vocabs_from_files(file, interDict, useEntities = False))
    for fdic in rets:
        keys = set(vocDict.keys())   
        for fword in fdic.keys():         
            if fword not in keys:                
                vocDict[fword] = fdic[fword]
                keys.add(fword) 
            else:
                vocDict[fword] += fdic[fword]
        dicList.append(fdic)                        
        fileCount += 1

    X = np.zeros((fileCount, len(vocDict)), dtype=int)
    print('X shape:' + str(X.shape))
    row_idx = 0
    vKeys = vocDict.keys()

    for dicti in dicList:
        for key in dicti.keys():
            col_idx = vKeys.index(key)            
            X[row_idx, col_idx] = dicti[key]
        row_idx += 1
    return (X, vKeys, titles)

def fit(X, vocab, titles, num_topics=15):
    model = lda.LDA(n_topics=num_topics, n_iter=200, random_state=1)
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
    print('numFiles: ' + str(numFiles))
    for n in range(numFiles):
        print('accessing doc topic ' + str(n))
        topic_most_pr = doc_topic[n].argmax()
        #print("{0} file most likely: {1}".format(n, topic_most_pr))
        #print("\t with: {0}", doc_topic[n][topic_most_pr])
        #print('most probable topic is:' + str(topic_most_pr))
        topic_files_dict[topic_most_pr].append(titles[n])  
    
    for n in range(num_topics):
        print("topic {0} len: {1}".format(n, len(topic_files_dict[n])))
        if len(topic_files_dict[n]) > 1:
            n_X, n_vocab, n_titles = build(files=topic_files_dict[n],intersect=True)
            print("X: {0}, v: {1}".format(len(n_X), len(n_vocab)))
            if len(n_X) > 0 and len(n_vocab) > 0:
                if len(n_X) == len(X) and len(n_vocab) == len(vocab):
                    print("FOUND LEAF TOPIC FOR ARTICLES:")
                    print("TOPIC {0}".format(n))
                    for f in X:
                        print("\t{0}".format(f))
                else:
                    fit(n_X, n_vocab, n_titles)

if __name__ == "__main__":
    dir_path = loc.news_dir
    files = fi.getTopLevelFiles(dir_path)
    X, vocab, titles = build(files=files,intersect=True)
    fit(X, vocab, titles)
        
        
        
        