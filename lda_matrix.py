from __future__ import division, print_function

import numpy as np
import itertools, io

from os import walk, path
import local as loc
import file_io as fi

from collections import OrderedDict
import text_manip as tm

import pos
from textclean.textclean import textclean

@profile
def vocab_from_file(raw_fpath, vocDict = dict(), vocab = [], intersect = True, interDict = dict(), isHTML = False):
    file_path = path.abspath(raw_fpath)
    print('building vocabulary for file:')
    print(file_path)     
    with io.open(file_path, 'rU', encoding='utf-8') as input:  
        if isHTML:
            text = tm.html_to_words(input.read())
            text = unicode(text, 'utf-8')
            text = textclean.clean(text)
            text = removeNonEntities(text) 
            keys = set(interDict.keys())           
            for word in text.split(): 
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

@profile
def removeNonEntities(text):
    text_nouns = ''
    for sent in pos.get_sentences(text):
        sent_nouns = pos.get_nouns(sent)
        text_nouns += ' '.join(sent_nouns)
    return text_nouns

@profile
def build(raw_dpath = loc.news_dir, extension ='htm', recurse = False, intersect = True, intersector_path = loc.intersector_path, interDict = dict()):
    dir_path = path.abspath(raw_dpath)                   
    vocDict = OrderedDict()
    vocab = []  
    if intersect:
        interDict = vocab_from_file(raw_fpath = intersector_path, intersect = False)[0]
    fileCount = 0
    XList = []
    for file in fi.getTopLevelFiles(dir_path):
        fdic, fvoc = vocab_from_file(raw_fpath = file, vocDict = OrderedDict(), vocab = vocab, intersect = intersect, interDict = interDict, isHTML = True)            
        print("{0} <-> {1}".format(len(vocab), len(fvoc)))
        #vocab.extend(fvoc)
        new_words = ()   
        keys = set(vocDict.keys())     
        for fword in fdic.keys():
            if fword not in keys:
                new_words += (fword,fdic[fword])                
                vocDict[fword] = fdic[fword]
            else:
                vocDict[fword] += fdic[fword]
        #add to x
        XList.append(fdic)                        
        fileCount += 1
    X = np.zeros((fileCount, len(vocDict)), dtype=int)  
    row_idx = 0
    vKeys = vocDict.keys();
    for dicti in XList:
        for key in dicti.keys():
            col_idx = vKeys.index(key)            
            X[row_idx, col_idx] = dicti[key]
        row_idx += 1
    return (X, vocab)

if __name__ == "__main__":
    build()
        