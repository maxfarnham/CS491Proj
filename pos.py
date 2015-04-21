import nltk, string
from pattern.en import tag

NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']

@profile
def tag_sentence(sentence): 
	return tag(sentence)

@profile
def get_sentences(text):
	# todo - lazy load sentence detector
	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	return sent_detector.tokenize(text)

@profile
def get_nouns(sentence): 
	tagged_sentence = tag_sentence(sentence)
	return [word if pos in NOUNS else '' for word,pos in tagged_sentence]