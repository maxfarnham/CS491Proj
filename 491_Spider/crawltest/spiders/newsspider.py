from pattern.vector import SVM
from mltools import *
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from scrapy.contrib.linkextractors import LinkExtractor
from urlparse import urlparse
import scrapy

frameSVM = train_classifier(SVM(), frame_features, get_training_data())
MAX_LINKS = 100000

class NewsSpider(CrawlSpider):
    name = "news"
    #allowed_domains = ["reuters.com"]
    start_urls = ["http://www.dmoz.org/"]
    #allowed_domains = ["arstechnica.com"]
    #start_urls = ["http://arstechnica.com/"]
    total_links = 0

    def remove_querystring(url):
	    o = urlparse(url)
	    new_url = o.scheme + "://" + o.netloc + o.path
	    return new_url

    rules = (
			    Rule(LinkExtractor(allow=(r'.*',), process_value=remove_querystring), callback='test_link', follow=True),
		    )

    def test_link(self, response):
	    #try:
		    if NewsSpider.total_links < MAX_LINKS:
			    print NewsSpider.total_links
			    doc = frame_features(response.body)
			    if frameSVM.classify(doc) == 1:
				    with open('frameSVM_news.txt', 'a') as f:
					    f.write(response.url + '\n')
			    else:
				    with open('frameSVM_notnews.txt', 'a') as f:
					    f.write(response.url + '\n')
			    NewsSpider.total_links += 1
		   # else:
			  #  raise CloseSpider('{0} links classified'.format(NewsSpider.total_links))
	    #except Exception, e:
		   # if isinstance(e, CloseSpider):
			  #  raise e
		   # else:
			  #  print "skipping {0} because {1}".format(response.url, e.message)