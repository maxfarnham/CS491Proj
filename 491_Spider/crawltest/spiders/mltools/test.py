from pageparser   	import PageParser
import urllib2
import io

if __name__ == '__main__':
	URL = 'http://arstechnica.com/science/2013/05/22/merger-of-ancient-galaxies-could-explain-the-origin-of-todays-giants/'
	resp = urllib2.urlopen(URL)
	html = resp.read()
	with io.open('test.txt', 'w+', encoding='utf-8') as f:
		f.write(PageParser.parse(html))