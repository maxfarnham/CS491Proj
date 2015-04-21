from __future__ import division, print_function

import numpy as np
import itertools

from os import walk, path
import local as loc
import file_io as fi

from collections import OrderedDict
import text_manip as tm

@profile
def vocab_from_file(raw_fpath, vocDict = dict(), vocab = [], intersect = True, interDict = dict(), isHTML = False):
    file_path = path.abspath(raw_fpath)
    print('building vocabulary for file:')
    print(file_path)   
    with open(file_path) as input:
        if isHTML:
            text = tm.html_to_words(input.read()) 
            keys = set(interDict.keys())           
            for word in text.split(): 
                if word in vocDict: 
                    vocDict[word] += 1
                else:  
                    if not intersect or word in keys:
                        vocDict[word] = 0
                        vocab.append(word) 
        else:
            for word in itertools.chain.from_iterable(line.split() for line in input):
                if not intersect or word in interDict.values():
                    if word not in vocDict:
                        vocDict[word] = 0
                        vocab.append(word)
                    else:
                        vocDict[word] += 1
    return (vocDict, vocab)

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
        vocab.extend(fvoc)
        new_words = ()        
        for fword in fdic.keys():
            if fword not in vocDict.keys():
                new_words += (fword,fdic[fword])                
                vocDict[fword] = fdic[fword]
            else:
                vocDict[fword] += fdic[fword]
        #add to x
        XList.append(fvoc)                        
        fileCount += 1
    X = np.zeros((fileCount, len(vocDict)), dtype=int)  
    row_idx = 0
    for x in XList:
        for kvp in x:
            col_idx = vocDict.keys().index(kvp[0])            
            X[row_idx, col_idx] = kvp[1]
        row_idx += 1
    return (X, vocab)

if __name__ == "__main__":
    build()
        