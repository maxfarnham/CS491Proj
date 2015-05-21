from pattern.vector import SVM
from mltools import *
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
import matplotlib.pyplot as plt
from urlparse import urlparse
from os import path
import scrapy
from mltools import datastructures as ds
from scrapy.contrib.linkextractors import LinkExtractor
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
		import traceback, os.path
		top = traceback.extract_stack()[-1]
		print ', '.join([type(e).__name__, os.path.basename(top[0]), str(top[1])])
MAX_LINKS = 100000

class NewsSpider(CrawlSpider):
	name = "news"
	#allowed_domains = ["huffingtonpost.com"]
	start_urls = ["http://vice.com"]
	deny = ('softpedia',)
	total_links = 0
	#allowed_domains = ["arstechnica.com"]
	#start_urls = ["http://arstechnica.com/"]
	dg = initialize_graph()
	news_dests = []
	news_dest_top = 0
	def remove_querystring(url):
		o = urlparse(url)
		new_url = o.scheme + "://" + o.netloc + o.path
		return new_url
	rules = (
				Rule(LinkExtractor(allow=(r'.*',), deny=deny, process_value=remove_querystring), callback='process_node', follow=True),
			)
	def process_node(self, response):
		
		url = response.url
		isNews = False

		with open('crawl_log.txt', 'a') as f:
			f.write('visiting ' + url + '\n')
			f.write('\tpriority is ' + str(self.dg.ordered_links[response.url]) + '\n')
			self.dg.visited.add(str(url))
			f.write('\tthe current length of the visited set is : ' + str(len(self.dg.visited)) + '\n')
			if self.total_links < MAX_LINKS:
				dests = []
				reqs = []
				for link in LinkExtractor().extract_links(response):
					dest = link.url
					dests.append(dest)
					req = self.make_requests_from_url(dest)
					req.callback = self.process_node					
					if dest in set(self.dg.ordered_links.keys()):
						req.priority = -1
						self.dg.ordered_links[dest] = -1
					else:
						reqs.append(req)
				add_edges(self.dg,url,dests)
				features = {}
				if featuresOn:
					features = {'outdegree' : len(dests)}
				try:
					doc = frame_features(response.body,features=features, dg=self.dg)
				except UnicodeDecodeError:
					try:
						doc = frame_features(unicode(response.body),features=features, dg=self.dg)
					except UnicodeDecodeError:
						with open('dadbods.txt','a+') as db:
							db.write(url+'\n')
						return []
				if frameSVM.classify(doc) == 1:
					isNews = True
					with open('frameSVM_news.txt', 'a') as nf:
						self.news_dests+=dests
						nf.write(response.url + '\n')
						nf.write('\t' + 'outdegree : ' + str(doc.vector['outdegree']) + '\n')
				else:
					with open('frameSVM_notnews.txt', 'a') as nf:
						nf.write(response.url + '\n')
						nf.write('\t' + 'outdegree : ' + str(doc.vector['outdegree']) + '\n')
				if isNews:
					self.crawler
					for req in reqs:
						if req.priority != -1:		
							self.dg.ordered_links[req.url] = self.dg.ordered_links[req.url] + 1
							req.priority = self.dg.ordered_links[req.url]
							#with open('recursion.txt','a') as rf:
								#rf.write('bout to recurse on: ' + some_request.url + '\n')
								#process_node(self, some_request)
								#rf.write('can u smell what the re is cursin! \n')
				reqs = [i for i in reqs if i.priority != -1]
				NewsSpider.total_links += 1
				req = scrapy.http.Request(url)
				whether_it_was = " it was "
				if not isNews:
					whether_it_was = " it wasn't "
				f.write('crawled ' + url + whether_it_was + ' news ' + '\n')
				f.write('returning reqs\n')
				#plt.show()
				#nx.draw(self.dg)
				return reqs


		#		total_links_observed = len(self.dg.ordered_links.keys())
		#		if len(self.news_dests) > self.news_dest_top and total_links_observed % 2 == 0:
		#			f.write('starting requests on news link: ' + self.news_dests[self.news_dest_top] + '\n')
		#			self.news_dest_top += 1		
		#			req = self.make_requests_from_url(self.news_dests[self.news_dest_top-1])
		#			#self.start_urls = [self.news_dests[self.news_dest_top-1]]
		#			try:
		#				req.priority = self.news_dest_top+1
		#				req.callback = self.process_node
		#				#self.start_urls = list[news_dests[news_dest_top-1]]
		#				#self.start_requests()
		#			except Exception as e:
		#				import traceback, os.path
		#				top = traceback.extract_stack()[-1]
		#				print ', '.join([type(e).__name__, os.path.basename(top[0]), str(top[1])])
		#				import time
		#				sleep(15)
		#				#pass
		#		else:
		#			f.write('starting requests on dg top: ' + self.dg.ordered_links.items()[total_links_observed-1][0] + '\n')
		#			req = self.make_requests_from_url(self.dg.ordered_links.items()[total_links_observed-1][0])
		#			#self.start_urls = [self.dg.ordered_links.items()[total_links_observed-1][0]]
		#			req.callback = self.process_node
		#			req.priority = 1
		#plt.show()
		#nx.draw(self.dg)
		#self.dg.visited.update(url)
		#return reqs
		#				#self.start_urls = [dg.ordered_links.items()[total_links_observed-1]]
		#				#self.start_requests()
		#	#nx.draw_networkx_edge_labels(pos=)

		#	# else:
		#		#  raise CloseSpider('{0} links classified'.format(NewsSpider.total_links))
		##except Exception, e:
		#	# if isinstance(e, CloseSpider):
		#		#  raise e
		#	# else:
		#		#  print "skipping {0} because {1}".format(response.url, e.message)
