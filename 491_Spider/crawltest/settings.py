# -*- coding: utf-8 -*-

# Scrapy settings for crawltest project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'crawltest'

SPIDER_MODULES = ['crawltest.spiders']
NEWSPIDER_MODULE = 'crawltest.spiders'
CONCURRENT_REQUESTS = 75

#######################################################################################################################################################
#DEPTH_PRIORITY = 1
#SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
#SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'
#######################################################################################################################################################

#built-ins range from 100-900
DOWNLOADER_MIDDLEWARES = {

'crawltest.middlewares.CustomRetryMiddleware': 120,
#'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': None,
#'scrapy.contrib.downloadermiddleware.redirect.MetaRefreshMiddleware': None,

'crawltest.middlewares.IgnoreDupes': 99,

'crawltest.middlewares.RetryMiddleware': 500,
'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': None,
}

#built-ins range from 50-900
SPIDER_MIDDLEWARES = {
	'crawltest.middlewares.FilterRequests': 48,
	#'crawltest.middlewares.PreventRedirects': 49,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawltest (+http://www.yourdomain.com)'

#seems hacky, but the redirects are killin me
HTTPCACHE_IGNORE_HTTP_CODES = [301,302]