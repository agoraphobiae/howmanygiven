# downloader

import mechanize
import re

def getPage(url):
	br = mechanize.Browser()
	br.addheaders = [('User-Agent',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36')]

	r = br.open(url)
	html = r.read()

	return html


def numword(document):
	counter = 0
	matches = re.findall(r'fuck[\w]*', document)
	for i in matches:
		counter++
	return counter