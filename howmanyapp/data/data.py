import os
import re
import string
import sys
from string import ascii_letters

def load_sentiments(file_name="sentiments.csv"):
    """Read the sentiment file and return a dictionary containing the sentiment
    score of each word, a value from -1 to +1.
    """
    sentiments = {}
    for line in open(file_name):
        word, score = line.split(',')
        sentiments[word] = float(score.strip())
    return sentiments

word_sentiments = load_sentiments()


def extract_words(document):
	"""gets rid of non-letter stuff"""
	for i in document:
		if i not in ascii_letters:
			document = document.replace(i, " ")
	document = document.split()
	return document

def analyze_doc(document):
	"""Outputs value of document and also documentation makes you feel smart lol"""
	total = 0
	count = 0
	newdoc = extract_words(document)
	for i in newdoc:
		value = word_sentiments.get(i, 0)
		if value != 0:
			total += value
			count += 1
	average = 0
	if count != 0:
		average = total/count
	return average