from pattern.vector import Document, NB, Vector, kfoldcv, SVM
from pageparser   	import PageParser
import local as sett
import random
import os
import io
import operator
import functools

def raw_text_features(text, t=-1):
	if t != -1:
		doc = Document(PageParser.parse(text), type=t, stopwords=True)
	else:
		doc = Document(PageParser.parse(text), stopwords=True)
	return doc

def frame_features(text, t=-1):
	parsed_text = PageParser.parse(text)

	d = {
		 'periods': 0,
		 'commas': 0,
		 'questions': 0,
		 'exclamations': 0,
		 'whitespace': 0,
		 'letters': 0,
		 'longestword': 0
		}

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
		doc = Document(Vector(d), type=t)
		#print doc.vector
		#print "--vs--"
		return doc
	else:
		doc = Document(Vector(d))
		return doc

# generator for training data
def training_data():
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

def train_classifier(c, feat_ex, training_data, data_len):
	split_ratio = 0.67
	news_test = {}

	for label, fname, text in training_data:
		total_docs = 0
		try:
			if random.random() > split_ratio and total_docs < data_len * split_ratio: 
				doc = feat_ex(text, label)
				c.train(doc)
				total_docs += 1
			else:
				doc = feat_ex(text)
				if label not in news_test.keys():
					news_test[label] = []
				news_test[label].append((doc, fname))

		except Exception, e:
			# sometimes we'll get an encoding error, ignore this file
			print "skipping because {0}".format(e.message)		

	correct = 0
	for k in news_test.keys():
		for d, fname in news_test[k]:
			if c.classify(d)  == k:
				correct += 1

	lent = functools.reduce(operator.add, [len(news_test[k]) for k in news_test.keys()], 1)
	accuracy = (correct/float(lent)) * 100.0
	print "\tAccuracy: {0}%".format(accuracy)

if __name__ == '__main__':
	train_len = functools.reduce(operator.add, [len(os.listdir(d)) for d in [sett.not_news_dir, sett.news_dir]], 1)
	#print train_len

	print "Frame features with SVM:"
	frame_data = []
	for i,fname,text in training_data():
		frame_data.append(frame_features(text, i))

	print kfoldcv(SVM, frame_data, folds=10)

	print "Frame features with NB:"
	print kfoldcv(NB, frame_data, folds=10)

	print "BoW with Naive Bayes:"
	bag_data = []
	for i,fname,text in training_data():
		bag_data.append(raw_text_features(text, i))

	print kfoldcv(NB, bag_data, folds=10)

	#print "calculating with frame features..."
	#nb = train_classifier(NB(), frame_features, training_data(), train_len)
	#print "calculating with bag of words"
	#nb = train_classifier(NB(), raw_text_features, training_data(), train_len)
	