from pattern.vector import NB, SVM, Document, Vector, count
from pattern.text.en 	import tag
from pageparser   	import PageParser
import settings as sett
import random
import os
import io
import operator
import functools
import networkx as nx
import datastructures as ds
from collections import OrderedDict
from BeautifulSoup import BeautifulSoup, SoupStrainer
from settings import featuresOn as featuresOn
class DiGraph(nx.DiGraph):
	visited = set()
	domains = ds.DefaultOrderedDict(tuple)
	ordered_links = ds.DefaultOrderedDict(int)
	def url_to_index(self,url):
		if url in self.ordered_links:
			return self.ordered_links.keys().index(url)
		if self.ordered_links[url] == 0:
			self.ordered_links[url] = 0
		return self.ordered_links.keys().index(url)

def get_links(text):
	links = []
	for link in BeautifulSoup(text, parseOnlyThese=SoupStrainer('a')):
		try:
			for attr in link.attrs:
				if attr[0] == 'href' and attr[1] not in set(links):
					links.append(attr[1])
		except Exception as e:
			import traceback, os.path
			top = traceback.extract_stack()[-1]
			print ', '.join([type(e).__name__, os.path.basename(top[0]), str(top[1])])
			#pass
	return links
def raw_text_features(text, t=-1):
	if t != -1:
		doc = Document(PageParser.parse(text)[0], type=t, stopwords=True)
	else:
		doc = Document(PageParser.parse(text)[0], stopwords=True)
	return doc

def frame_features(text, t=-1, features = {}, dg=''):

	parsed_text, html_tag_counts = PageParser.parse(text)
	d = {
			'periods': 0,
			'commas': 0,
			'questions': 0,
			'exclamations': 0,
			'whitespace': 0,
			'letters': 0,
			'longestword': 0,
			'news': 0,
			'article': 0,
			'sale': 0,
			'you': 0,
			'I': 0,
			'me': 0
		}

	# add html tag counts
	d.update(html_tag_counts)
	# add pos tag counts
	d.update(count([pos for word,pos in tag(parsed_text)])) 

	longestWordLength = 0
	currentWordLength = 0
	currentWord = ''
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
			if currentWord.lower() == 'news':
				d['news'] += 1
			elif 'article' in currentWord.lower():
				d['article'] += 1
			elif currentWord.lower() == 'sale':
				d['sale'] += 1     
			elif currentWord == 'I':
				d['I'] += 1    
			elif currentWord.lower() == 'you':
				d['you'] += 1   
			elif currentWord.lower() == 'me':
				d['me'] += 1                                                                                                 
			currentWordLength = 0
			currentWord = ''
		else:
			currentWordLength += 1
			currentWord += letter
	d = ds.merge_dicts(d, features)
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
			features = {}
			if featuresOn:
				features = {'outdegree' : len(get_links(text))}
			doc = feat_ex(text, label, features)
			c.train(doc)
			
		except Exception, e:
			# sometimes we'll get an encoding error, ignore this file
			print "skipping because {0}".format(e.message)

	print "classifier trained!"
	return c 

def make_edge_list(dg,src,dests=[]):
	out_edges = []
	src_index = dg.url_to_index(src)
	dg.add_node(src_index)
	for dest in dests:
		edge = (src_index,dg.url_to_index(dest))
		out_edges.append(edge) 
	return out_edges

def add_edges(dg,src,dests=[]):
	dg.add_edges_from(make_edge_list(dg,src,dests=dests))

def initialize_graph(data=[],datafunc=None):
	def foo(data):
		return data
	if datafunc is None:
		datafunc = foo
	dg = DiGraph(data=datafunc(data=data))
	return dg
