import grammarcheck as gc
import local as loc
import nltk

def recognize_entities(text):
	tokenized = nltk.word_tokenize(text)
	tagged = nltk.pos_tag(tokenized)
	print tagged
	namedEnt = nltk.ne_chunk(tagged, binary=True)
	namedEnt.draw()

	

if __name__ == "__main__":
	text='Arizona Governor Vetoes Bill That Would Have Shielded Officers In Fatal Shootings'
	recognize_entities(text)