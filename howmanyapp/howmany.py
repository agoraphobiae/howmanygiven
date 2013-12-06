# downloader

import mechanize
from bs4 import BeautifulSoup
from bs4.element import Comment

from data import HowManyDoc, SentimentDoc

def count_in_page(url, s):
	print "URL: ", url
	br = mechanize.Browser()
	br.addheaders = [('User-Agent',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36')]

	r = br.open(url)
	d = HowManyDoc( innertext_from_html(r.read()) )

	return d.numword(s)

def analyze_page(url):
	print "URL: ", url
	br = mechanize.Browser()
	br.addheaders = [('User-Agent',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36')]

	r = br.open(url)
	pagetext = innertext_from_html(r.read())
	d = SentimentDoc(pagetext)

	d.rank_words()
	d.numword('fuck')
	d.analyze()

	return d


def innertext_from_html(html):
	soup = BeautifulSoup(html, from_encoding="utf-8")
	[unwantedtag.extract() for unwantedtag in soup(['script', 'style'])]
	alltxt = [txt for txt in soup.find_all(text=True) if not isinstance(txt, Comment)]
	# print u' '.join(alltxt)
	return u' '.join(alltxt)


def cleanQueryName(path):
	"""
	>>> cleanQueryName("http://reddit.com")
	'reddit.com'
	>>> cleanQueryName("reddit.com")
	'reddit.com'
	>>> cleanQueryName("http://u.reddit.com/r/buildapcsales")
	'r/buildapcsales'
	"""
	# TODO
	return path
