import re
import string
import sys
from string import ascii_letters, digits

from howmany import HowManyDoc

class SentimentDoc(HowManyDoc):
	sentiment_dict = "data/sentiments.csv"

	def __init__(self, document):
		"""Setup the SentimentDoc, by loading the default sentiment_dict
		and extract_words-ing from the given document param"""
		# initialize
		self.maxphrase = ('null', 0)
		self.word_sentiments = {}
		self.sentiment_value = 'null'

		# need self.document
		HowManyDoc.__init__(self, document)

		# setup calls
		self.extract_words()
		self.load_sentiments() # will update word_sentiments

	def load_sentiments(self, filename=sentiment_dict):
		"""Read the sentiment file and set self.word_sentiments to a 
		dictionary containing the sentiment score of each word, a 
		value from -1 to +1.
		"""
		for line in open(filename):
			word, score = line.split(',')
			curlen = len(word.split())
			if curlen > self.maxphrase[1]:
				self.maxphrase = (word, curlen)

			self.word_sentiments[word] = float(score.strip())
		#print self.maxphrase

	def extract_words(self):
		"""gets rid of non-letter stuff"""
		# TODO: make faster, not O(n^2)
		for i in self.document:
			if i not in ascii_letters and i not in digits:
				self.document = self.document.replace(i, " ")
		self.document = self.document.split()

	def analyze(self):
		"""Calculates a sentiment value of document, a measure of it's average
		emotion, from -1 to 1, with 1 being positive.

		sentiment = sum(values) / num(values)

		Phrase algorithm:
		We keep a list of the most recent n words, where n is the length
		of the longest phrase we're looking for (should be 7). We go down this
		list looking for phrases as follows:

		1,2,3,4 -> not a phrase
		2,3,4 -> not a phrase
		3,4 -> phrase match, rollback 3

		On a phrase match, we rollback the counter and the sentiment values
		of the words in the phrase, so we don't double count. Phrases count
		for one counter increment.

		>>> SentimentDoc("101").analyze()
		-0.25
		>>> SentimentDoc("abandon").analyze()
		-0.375
		>>> SentimentDoc("a priori").analyze()
		0.25
		>>> SentimentDoc("william carlos williams").analyze()
		0.375
		>>> SentimentDoc("william carlos 101 williams").analyze()
		-0.25
		>>> SentimentDoc("william carlos williams a priori").analyze()
		0.3125
		>>> SentimentDoc("william carlos williams abandon a priori").analyze()
		0.08333333333333333
		>>> SentimentDoc("").analyze()
		0
		"""
		total = 0
		count = 0
		lastnwords = []

		for word in self.document:
			# print "WORD", word
			value = self.word_sentiments.get(word, 0)
			if value:
				total += value
				count += 1

			lastnphrase = ' '.join(s[0] for s in lastnwords)
			lastnphrase += ' ' + word
			lastnphrase = lastnphrase.strip()

			# print "PHRASE", lastnphrase, "WORD", word
			lastnwordschecker = lastnwords[:] # we are going to mutate this list, so lets make a copy

			# phrase loop
			while lastnphrase != word:
				phrasevalue = self.word_sentiments.get(lastnphrase, 0)
				# print "LASTNPHRASE", lastnphrase
				if phrasevalue and len(lastnphrase.split()) > 1:
					# print "LASTNPHRASE inside check", lastnphrase
					for phraseword,v in lastnwordschecker:
						# rollback our values
						# print phraseword, v
						total -= v
						if v:
							# print "asdf"
							count -= 1
					total += phrasevalue
					# print "PHRASEVAL", phrasevalue
					count += 1
					# print "TOTAL", total
					lastnwordschecker = []
					break

				# take off first word and check the rest
				lastnphrase = lastnphrase[lastnphrase.find(' ')+1:]
				lastnwordschecker.pop(0)


			# didnt find phrase, no need to reset,
			# keep lookin!
			lastnwords.append( (word, value) )
			if len(lastnwords) > self.maxphrase:
				lastnwords.pop(0)
			# print "TOTAL", total, "COUNT", count

		self.sentiment_value = 0
		if count:
			self.sentiment_value = total/count
			# print average
		return self.sentiment_value
