# downloader

import mechanize
import re

from collections import OrderedDict

def countInPage(url, s):
	print "URL: ", url
	br = mechanize.Browser()
	br.addheaders = [('User-Agent',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36')]

	r = br.open(url)
	html = r.read()

	return numword(html, s)

def numword(document, s):
	counter = 0
	matches = re.finditer(r'%s[\w]*'%(s), document)
	for i in matches:
		counter += 1
	return counter

def rankWords(document, topnum=5, commonignore=True):
	"""Gets the longest word and the topnum most used words"""
	wordcount = {}
	wordregex = r'\b[\w][\w]*\b'
	matches = re.finditer(wordregex, document)

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
	return wordcount, longestword
