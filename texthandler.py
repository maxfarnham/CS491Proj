import nltk
from textblob 		  import Blobber, TextBlob
from textblob.taggers import PatternTagger
from textblob.parsers import PatternParser
TAGS = {
	'NOUN': ['NN', 'NNS', 'NNP', 'NNPS']
}

class TextHandler:
    def __init__(self, text):
        self._raw_text = text
        self._sentences = None
        self._blobber = Blobber(parser = PatternParser(), pos_tagger = PatternTagger())
        self._text_dirty = False

    def __str__(self):
        return self._raw_text

    @property
    def sentences(self):
        if self._sentences is None or self._text_dirty:
            self._sentences = []
            sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
            for sent in sent_detector.tokenize(self._raw_text):
                self._sentences.append(self._blobber(sent))
        return self._sentences

    @property
    def words(self):
        words = []
        for sent in self.sentences:
            words.extend(map(lambda (word,pos): word, sent.tags))
        return words

    # remove all tags if they don't satisfy a certain func
    def filter_words(self, func):
        new_text = ''
        for sent in self.sentences:
            for word,pos in sent.tags:
                if func((word,pos)):
                    new_text += ' ' + word
        self._raw_text = new_text
        self._text_dirty = True