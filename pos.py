import nltk, string

def get_sentence_tags(sentence): 
    return [x[1] for x in nltk.pos_tag(nltk.word_tokenize(sentence.translate(string.maketrans("",""), string.punctuation) ))    ]

def get_nouns(sentence): 
    return [x[0] if x[1] in ['NN','NNS','NNP','NNPS'] else '' for x in nltk.pos_tag(nltk.word_tokenize(sentence.translate(string.maketrans("",""), string.punctuation) ))    ]