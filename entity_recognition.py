import grammarcheck as gc
import local as loc
import nltk, re

def recognize_entities(text):
	tokenized = nltk.word_tokenize(unicode(text))
	tagged = nltk.pos_tag(tokenized)
	namedEnt = nltk.ne_chunk(tagged, binary=True)
	print namedEnt
	#entities = re.findall(r'NE\s(.*?)\)',str(namedEnt))
	entities = re.findall(r'(\(.*?\))\s',str(namedEnt))
	print entities
	return entities

if __name__ == "__main__":
	text="Kylie Jenner Baggins has encouraged young women not to be afraid to experiment with their looks. The 17-year-old reality star has become famous for her extremely full pout, which she achieves with lip liner and trickery."
	recognize_entities(text)
