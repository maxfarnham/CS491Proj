from __future__ import division
from collections import defaultdict
import pattern
import urllib2
from os import path
import os
import io
from pattern.text.en import parse
from textblob import TextBlob, Blobber
from textblob.parsers import PatternParser
from textblob.taggers import PatternTagger
#user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US)
#AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
#headers = { 'User-Agent' : user_agent }
dir = 'downloads'
fname = path.abspath('frameSVM_news.txt')
def arrange_arts_by_year():
	with open(fname,'r') as f:
		d = defaultdict(list)
		s = f.readlines()
		for line in s:
			for year in range(2005,2016):
				if str(year) in line:
					d[year].append(line)
		return d

def download_sources():
	d = arrange_arts_by_year()	
	years = set(d.keys())
	source_dic = defaultdict(list)
	i = 0
	for year in years:
		for art in d[year]:
			try:
				req = urllib2.Request(art)
				response = urllib2.urlopen(req)
				#source_dic[year].append(response.read())
				with open('downloads/' + str(year) + '-' + str(i) + '.html','w+') as f:
					f.write(response.read())
				i += 1
			except Exception, e:
				pass
	return source_dic
def computeSentiment():
	d = defaultdict(list)
	opinion = 0
	years = {}
	for file in os.listdir(dir):
		print file
		for year in range(2010,2016):
				if str(year) in file:
					try:
						with io.open(dir + '\\' + file,'r', encoding='utf-8') as f:
							if not year in years.keys():
								years[year] = []
							years[year].append(TextBlob(unicode(f.read())).sentiment.polarity)
					except Exception, e:
						# forget the ones we get errors decoding
						print "skip because {0}".format(e.message)
						pass
	return years
if __name__ == "__main__":
	d = computeSentiment()
	for year in d.keys():
		avg = sum(d[year])/len(d[year])
		print "avg sent for year {0}: {1}".format(year, avg)
	while(True):
		pass