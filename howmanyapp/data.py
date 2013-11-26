import re
import string
import sys
from string import ascii_letters, digits

maxphrase = ('null', 0)

def load_sentiments(file_name="data/sentiments.csv"):
    """Read the sentiment file and return a dictionary containing the sentiment
    score of each word, a value from -1 to +1.
    """
    sentiments = {}
    for line in open(file_name):
        word, score = line.split(',')
        curlen = len(word.split())
        if curlen > maxphrase[1]:
        	global maxphrase
        	maxphrase = (word, curlen)

        sentiments[word] = float(score.strip())
    print maxphrase
    return sentiments

# fuck this is gross
word_sentiments = load_sentiments()


def extract_words(document):
	"""gets rid of non-letter stuff"""
	for i in document:
		if i not in ascii_letters and i not in digits:
			document = document.replace(i, " ")
	document = document.split()
	return document

def analyze_doc(document):
	"""Outputs value of document and also documentation makes you feel smart lol
	Phrases count as 1 "value" word, and we rollback counting of values/increments 
	if we find a phrase

	>>> analyze_doc("101")
	-0.25
	>>> analyze_doc("abandon")
	-0.375
	>>> analyze_doc("a priori")
	0.25
	>>> analyze_doc("william carlos williams")
	0.375
	>>> analyze_doc("william carlos 101 williams")
	-0.25
	>>> analyze_doc("william carlos williams a priori")
	0.3125
	>>> analyze_doc("william carlos williams abandon a priori")
	0.0833333333
	>>> analyze_doc("")
	0
	"""
	total = 0
	count = 0
	newdoc = extract_words(document)
	lastnwords = []

	for word in newdoc:
		value = word_sentiments.get(word, 0)
		if value:
			total += value
			count += 1

		lastnphrase = ' '.join(s[0] for s in lastnwords)
		lastnphrase += ' ' + word
		lastnphrase = lastnphrase.strip()

		phrasevalue = word_sentiments.get(lastnphrase, 0)
		print lastnphrase
		if phrasevalue and len(lastnphrase.split()) > 1:
			# print "LOL", lastnphrase
			for phraseword,v in lastnwords:
				# rollback our values
				total -= v
				if v:
					count -= 1
			total += phrasevalue
			count += 1
			# print total
			lastnwords = []
		else:
			# didnt find phrase, no need to reset,
			# keep lookin!
			lastnwords.append( (word, value) )
			if len(lastnwords) > maxphrase:
				lastnwords.pop(0)

		print value, count

	average = 0
	if count:
		average = total/count
		# print average
	return average