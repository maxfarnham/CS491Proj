from pattern.vector import NB, SVM, Document, Vector, count
from pattern.en 	import tag
from pageparser   	import PageParser
import settings as sett
import random
import os
import io
import operator
import functools

def raw_text_features(text, t=-1):
	if t != -1:
		doc = Document(PageParser.parse(text)[0], type=t, stopwords=True)
	else:
		doc = Document(PageParser.parse(text)[0], stopwords=True)
	return doc

def frame_features(text, t=-1):
	parsed_text, html_tag_counts = PageParser.parse(text)

	d = {
		 'periods': 0,
		 'commas': 0,
		 'questions': 0,
		 'exclamations': 0,
		 'whitespace': 0,
		 'letters': 0,
		 'longestword': 0
		}

	# add html tag counts
	d.update(html_tag_counts)
	# add pos tag counts
	#d.update(count([pos for word,pos in tag(parsed_text)])) 

	longestWordLength = 0
	currentWordLength = 0
	for letter in parsed_text:
		d['letters'] += 1
		if letter == '.':
			d['periods'] +=1
		if letter == ',':
			d['commas'] +=1
		if letter == '?':
			d['questions'] +=1
		if letter == '!':
			d['exclamations'] +=1
		if letter == ' ':
			d['whitespace'] += 1
			if currentWordLength > d['longestword']:
				d['longestword'] = currentWordLength
			currentWordLength = 0            
		else:
			currentWordLength += 1

	if t != -1:
		return Document(Vector(d), type=t)
	else:
		return Document(Vector(d))

# generator for training data
def get_training_data():
	for i,d in enumerate([sett.not_news_dir, sett.news_dir]):
		files = os.listdir(d)
		for f in files:
			if f.split('.')[-1] in ['htm', 'html']:
				#print f
				try:
					with io.open(d + '\\' + f, 'r', encoding='utf-8') as htmlfile:
						yield (i, f, htmlfile.read())
				except Exception, e:
					# skip any training files that don't want to load
					pass

def train_classifier(c, feat_ex, training_data):
	print "training classifier..."

	for label, fname, text in training_data:
		total_docs = 0
		try:
			doc = feat_ex(text, label)
			c.train(doc)

		except Exception, e:
			# sometimes we'll get an encoding error, ignore this file
			print "skipping because {0}".format(e.message)

	print "classifier trained!"
	return c
