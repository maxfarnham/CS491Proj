from __future__ import division, print_function

import numpy as np
import lda
import itertools

from os import walk, path
import local as loc
import file_io as fi

from collections import OrderedDict

def vocab_from_file(raw_fpath, vocDict = dict(), vocab = (), intersect = True, interDict = dict(), isHTML = False):
    file_path = path.abspath(raw_fpath)
    with open(file_path) as input:
        for word in itertools.chain.from_iterable(line.split() for line in input):
            if not intersect or word in interDict.values():
                if word not in vocDict:
                    vocDict[word] = 0
                    vocab += (word,)
                else:
                    vocDict[word] += 1
    return (vocDict, vocab)

def build(raw_dpath = loc.news_dir, extension ='htm', recurse = False, intersect = True, intersector_path = loc.intersector_path, interDict = dict()):
    dir_path = path.abspath(raw_dpath)
    vocDict = OrderedDict()
    vocab = ()   
    if intersect:
        interDict = vocab_from_file(raw_fpath = intersector_path, intersect = False)[0]
    fileNo = 0
    XList = []
    for file in fi.getTopLevelFiles(dir_path):
        print("constructing row for: " + file)
        fdic_fvoc_pair = vocab_from_file(raw_fpath = file, vocDict = OrderedDict(), vocab = vocab, intersect = intersect, interDict = interDict, isHTML = True)                
        vocab += fdic_fvoc_pair[1]
        new_words = ()        
        for fword in fdic_fvoc_pair[0].keys():
            if fword not in vocDict.keys():
                new_words += (fword,fdic_fvoc_pair[0].keys[fword])                
                print('\tnew word:\n' + fword)
                vocDict[fword] += fdic_fvoc_pair[0].keys[fword]
            else:
                vocDict[fword] += fdic_fvoc_pair[0].keys[fword]
        #add to x
        XList.append(fdic_fvoc_pair[0])                        
        fileNo += 1
    X = np.ndarray(fileNo, len(voctDict.keys()))  
    idx = 0
    for x in Xlist:
        for kvp in x:
            colIdx = vocDict.keys().index(kvp[0])            
            X[idx, colIdx] = kvp[1]
        idx += 1
    return (X, vocab)


        