# downloader

import mechanize
from bs4 import BeautifulSoup
import re

from collections import OrderedDict

class HowManyDoc:
	def __init__(self, plaintext):
		self.document = plaintext
		self.wordrank = OrderedDict()
		self.wordcount = {}
		self.longestword = ('null', 0)

	def rank_words(self, topnum=5, commonignore=True):
		"""Gets the longest word and the topnum most used words"""
		wordcount = {}
		wordregex = r'\b[\w][\w]*\b'
		matches = re.finditer(wordregex, self.document)

		null = ('null', 0)
		longestword = null
		commonwords_ignore = ('the', 'and', 'of', 'a', 'to', 'on', 'is', 'that', 'be')

		for word in matches:
			word = word.group()
			if word in wordcount:
				wordcount[word] += 1
			else:
				wordcount[word] = 1

			if len(word) > longestword[1]:
				longestword = (word, len(word))

		topn = [null for _ in xrange(topnum)]
		for k,v in wordcount.items():
			if commonignore and k not in commonwords_ignore:
				for i in xrange(len(topn)):
					if v > topn[i][1]:
						topn.insert( i, (k,v) )
						topn.pop()
						break

		# order by greatest occurence first
		wordcount = OrderedDict(topn)
		self.wordrank = wordcount
		self.longestword = longestword

	def numword(self, s):
		"""Counts the occurences of s in self.document"""
		counter = 0
		matches = re.finditer(r'%s[\w]*'%(s), self.document)
		for i in matches:
			counter += 1
		self.wordcount[s] = counter

	def find_sentiment():
		pass



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
	d = HowManyDoc(pagetext)
	s = SentimentDoc(pagetext)

	d.rank_words()
	d.numword('fuck')
	s.analyze()

	return d


def innertext_from_html(html):
	soup = BeautifulSoup(html, from_encoding="utf-8")
	return u' '.join(soup.findAll(text=True))


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
