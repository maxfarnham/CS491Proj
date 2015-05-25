from __future__ import division
from pattern.vector import SVM
from mltools import *
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
import matplotlib.pyplot as plt
from urlparse import urlparse
from scrapy.utils.httpobj import urlparse_cached
from os import path
import random as rand
import scrapy
import traceback
from mltools import datastructures as ds
from scrapy.contrib.linkextractors import LinkExtractor
from inspect import currentframe, getframeinfo
try:
	import cPickle as pickle
except:
	import pickle

frameSVM = ''
if not os.path.isfile(sett.svmpickle):
	frameSVM = train_classifier(SVM(), frame_features, get_training_data())
	with open(sett.svmpickle, 'wb') as pkl_file:
		pickle.dump(frameSVM, pkl_file)
else:
	try:
		with open(sett.svmpickle, 'rb') as pkl_file:
			frameSVM = pickle.load(pkl_file)
	except Exception as e:
		log.exception(traceback.format_exc())
MAX_LINKS = 100000

class NewsSpider(CrawlSpider):
	name = "news"
	#allowed_domains = ["huffingtonpost.com"]
	start_urls = ["http://www.cnn.com/"]
	deny = ('softpedia',)
	dg = initialize_graph()
	total_links = 0
	total_positives = 0
	total_negatives = 0
	def remove_querystring(url):
		o = urlparse(url)
		new_url = o.scheme + "://" + o.netloc + o.path
		return new_url
	rules = (
				Rule(LinkExtractor(allow=(r'.*',), deny=deny, process_value=remove_querystring), follow=True),
			)
	def process_node(self, response, requests):
		def _make_edge_list(dg,src,dests=[]):
			out_edges = []
			src_index = dg.url_to_index(src)
			dg.add_node(src_index)
			for dest in dests:
				edge = (src_index,dg.url_to_index(dest))
				out_edges.append(edge) 
			return out_edges
		def _add_edges(dg,src,dests=[]):
			dg.add_edges_from(_make_edge_list(dg,src,dests=dests))
		def _modify_priority(request, spider=self, swap_value=None,add_value=0,scale_value=1):
			if swap_value == None:
				swap_value = request.priority
			request.priority = swap_value
			request.priority*=scale_value
			request.priority+=add_value
			spider.dg.ordered_links[request.url] = request.priority	
		def _priority_gauntlet(request):
			domain = urlparse_cached(request).hostname
			if domain not in self.dg.domains.keys():
				self.dg.domains[domain] = (0,0)
			domain_negatives = self.dg.domains[domain][0]
			domain_positives = self.dg.domains[domain][1]
			domains = self.dg.domains
			if domain not in domains:
				return
			if sum(domains[domain])/self.total_links > .25:
				_modify_priority(request, spider=self, swap_value=-3)
				randoid = rand.uniform(0,1)
				if domain_negatives == 0:
					return
				if self.total_positives > 0:
					if randoid < (domain_negatives/self.total_negatives)-(domain_negatives*domain_positives/self.total_positives*self.total_negatives):
						_modify_priority(request, spider=self, swap_value=-2)
						return
				if domain_positives and randoid < (domain_negatives/domain_positives):
					_modify_priority(request, spider=self, swap_value=-2)
					return
				return	
		log = Logger()		
		url = response.url
		domain = urlparse_cached(response).hostname
		log.visit_node(self,url)
		self.dg.visited.add(str(url))
		if self.total_links < MAX_LINKS:
			dests = []
			reqs = []
			for req in requests:
				dest = req.url
				dests.append(dest)	
				if req.url not in set(self.dg.ordered_links.keys()):
					reqs.append(req)
			_add_edges(self.dg,url,dests)
			requests = reqs
			features = {}
			if featuresOn:
				features = {'outdegree' : len(dests)}
			try:
				doc = frame_features(response.body,features=features, dg=self.dg)
			except Exception as e:
				log.exception(traceback.format_exc())
				if response.encoding == 'utf-8':
					try:
						data = response.body
						udata=data.decode("utf-8")
						asciidata=udata.encode("ascii","ignore")
						doc = frame_features(asciidata,features=features, dg=self.dg)
					except Exception as e:
						log.exception(traceback.format_exc())
						return requests		
			is_positive = frameSVM.classify(doc)
			log.record_classification(response, is_positive)
			log.memorialize_classification(self,response,is_positive,doc)
			if is_positive:
				self.total_positives+=1					
			else:
				self.total_negatives+=1
			self.total_links += 1
			#domain bookkeeping
			if domain not in self.dg.domains.keys():
				self.dg.domains[domain] = (0,0)
			domain_negatives = self.dg.domains[domain][0] 
			domain_positives = self.dg.domains[domain][1] 
			if is_positive:
				domain_positives += 1
				self.dg.domains[domain] = (domain_negatives,domain_positives)
			else:
				domain_negatives += 1
				self.dg.domains[domain] = (domain_negatives,domain_positives)
			log.record_domains(self,response)
			if is_positive:
				for req in requests:
					domain = urlparse_cached(req).hostname
					if req.priority > -1:
						if domain_positives > 0:
							_modify_priority(req, add_value=1)		
						_modify_priority(req, add_value=1)								
			for req in requests:
				_priority_gauntlet(req)
			#plt.show()
			#nx.draw(self.dg)	
		return (r for r in requests)
	def process(self, response):
		print 'visiting : ' + str(response.url)
		if self.total_links < MAX_LINKS:
			reqs = []
			for link in LinkExtractor().extract_links(response):
				req = self.make_requests_from_url(link.url)				
				reqs.append(req)
			return reqs
