import scrapy
from scrapy.exceptions import IgnoreRequest
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
		ConnectionRefusedError, ConnectionDone, ConnectError, \
		ConnectionLost, TCPTimedOutError

from scrapy import log
from scrapy.exceptions import NotConfigured
from scrapy.utils.response import response_status_message
from scrapy.xlib.tx import ResponseFailed
from scrapy.http import Request

from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.response import get_meta_refresh

MAX_LINKS = 100000
class FilterRequests(object):
	from crawltest.spiders import newsspider as ns
	def process_spider_output(self, response, result, spider):
		def _process_node(response, requests, spider):
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
			url = response.url
			isNews = False
			with open('crawl_log.txt', 'a') as f:
				f.write('visiting ' + url + '\n')
				f.write('\tpriority is ' + str(spider.dg.ordered_links[response.url]) + '\n')
				spider.dg.visited.add(str(url))
				f.write('\tthe current length of the visited set is : ' + str(len(spider.dg.visited)) + '\n')
				if spider.total_links < MAX_LINKS:
					dests = []
					reqs = []
					for req in requests:
						dest = req.url
						dests.append(dest)				
						if dest in set(spider.dg.ordered_links.keys()):
							req.priority = -1
							spider.dg.ordered_links[dest] = -1
						else:
							reqs.append(req)
					_add_edges(spider.dg,url,dests)
					features = {}
					if featuresOn:
						features = {'outdegree' : len(dests)}
					try:
						doc = frame_features(response.body,features=features, dg=spider.dg)
					except UnicodeDecodeError:
							return []
					if frameSVM.classify(doc) == 1:
						isNews = True
						with open('frameSVM_news.txt', 'a') as nf:
							spider.news_dests+=dests
							nf.write(response.url + '\n')
							nf.write('\t' + 'outdegree : ' + str(doc.vector['outdegree']) + '\n')
					else:
						with open('frameSVM_notnews.txt', 'a') as nf:
							nf.write(response.url + '\n')
							nf.write('\t' + 'outdegree : ' + str(doc.vector['outdegree']) + '\n')
					if isNews:
						spider.crawler
						for req in reqs:
							if req.priority != -1:		
								spider.dg.ordered_links[req.url] = spider.dg.ordered_links[req.url] + 1
								req.priority = spider.dg.ordered_links[req.url]
					reqs = [i for i in reqs if i.priority != -1]
					NewsSpider.total_links += 1
					req = scrapy.http.Request(url)
					whether_it_was = " it was "
					if not isNews:
						whether_it_was = " it wasn't "
					f.write('crawled ' + url + whether_it_was + ' news ' + '\n')
					f.write('returning reqs\n')
					#plt.show()
					#nx.draw(spider.dg)
					return reqs
		def _classify(response, spider):
			return spider
		def _keep(request, spider):
			if isinstance(request, Request):
				return request.url not in set(spider.dg.ordered_links.keys())
			return False
		if response.url in spider.dg.visited:
			return []	
		requests = (r for r in result if _keep(r, spider))
		return (r for r in spider._process_node(response, requests))
#class PreventRedirects(object):
#	def process_spider_output(self, response, result, spider):
#		def _mod(request, spider):
#			ret = ()
#			if isinstance(request, Request):
#				request.meta = {
#				'dont_redirect': True,
#				'handle_httpstatus_list': [301,302]
#			}
#				ret = request
#			return ret
#		return (_mod(r, spider) for r in result)
class CustomRetryMiddleware(RetryMiddleware):
	def process_response(self, request, response, spider):
		url = response.url
		response
		with open('redirects.txt', 'a+') as f:
			if response.status in [301, 307]:
				f.write("trying to redirect us: " + url + '\n')
				f.write('redirect %d' + str(response.status) + '\n')
				reason = 'redirect %d' %response.status 
				return self._retry(request, reason, spider) or response
			interval, redirect_url = get_meta_refresh(response)
			# handle meta redirect
			if redirect_url:
				f.write("trying to redirect us: " + url + '\n')
				f.write('redirect meta' + '\n')
				reason = 'meta'
				return self._retry(request, reason, spider) or response
			hxs = HtmlXPathSelector(response)
			# test for captcha page
			captcha = hxs.select(".//input[contains(@id, 'captchacharacters')]").extract()
			if captcha:
				f.write("trying to redirect us: " + url + '\n')
				f.write('redirect capcha' + '\n')
				reason = 'capcha'
				return self._retry(request, reason, spider) or response
		return response
class IgnoreDupes(object):
	def process_response(self, request, response, spider):
		with open('response_priorities.txt','a+') as f:
			f.write('priority: ' + str(request.priority) + '\n')
		if response.url in spider.dg.visited:			
			raise IgnoreRequest()
		else:
			return response

#disabled built-in middleware redefined below in order to extend support for adding retried urls to visited list in spider graph
class RetryMiddleware(object):

	# IOError is raised by the HttpCompression middleware when trying to
	# decompress an empty response
	EXCEPTIONS_TO_RETRY = (defer.TimeoutError, TimeoutError, DNSLookupError,
						   ConnectionRefusedError, ConnectionDone, ConnectError,
						   ConnectionLost, TCPTimedOutError, ResponseFailed,
						   IOError)

	def __init__(self, settings):
		if not settings.getbool('RETRY_ENABLED'):
			raise NotConfigured
		self.max_retry_times = settings.getint('RETRY_TIMES')
		self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))
		self.priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST')

	@classmethod
	def from_crawler(cls, crawler):
		return cls(crawler.settings)

	def process_response(self, request, response, spider):
		if 'dont_retry' in request.meta:
			return response
		if response.status in self.retry_http_codes:
			reason = response_status_message(response.status)
			return self._retry(request, reason, spider) or response
		return response

	def process_exception(self, request, exception, spider):
		if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
				and 'dont_retry' not in request.meta:
			return self._retry(request, exception, spider)

	def _retry(self, request, reason, spider):
		retries = request.meta.get('retry_times', 0) + 1
		spider.dg.visited.add(request.url)
		if retries <= self.max_retry_times:
			log.msg(format="Retrying %(request)s (failed %(retries)d times): %(reason)s",
					level=log.DEBUG, spider=spider, request=request, retries=retries, reason=reason)
			retryreq = request.copy()
			retryreq.meta['retry_times'] = retries
			retryreq.dont_filter = True
			retryreq.priority = request.priority + self.priority_adjust
			return retryreq
		else:
			log.msg(format="Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
					level=log.DEBUG, spider=spider, request=request, retries=retries, reason=reason)


