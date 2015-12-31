# -*- coding: utf-8 -*-
from pymongo import MongoClient
from bs4 import BeautifulSoup
from collections import OrderedDict
from datetime import datetime
import json
import requests
import os
import re

class Genesis():
	def __init__(self):
		self.col = MongoClient().genesis.test
		self.first_sentence_regex = r'^.*?[\.!\?…](?:\s|$)'

	# imports list of article IDs, returns list of IDs
	def __import_json(self, filename):
		return json.loads(open(filename, 'r').read(), object_pairs_hook=OrderedDict).values()

	# exports txt file
	# TODO: add to mongo
	def __export(self, tuples, source):
		path = '%s/%s-%s.txt' % (os.path.dirname(os.path.realpath(__file__)), source, str(datetime.now()))
		with open(path, 'w') as f:
			for url, sentence in tuples:
				f.write('%s\n%s\n\n' % (url, sentence))

	# medium articles
	def medium(self):
		ids = self.__import_json('medium-12-30-15.json')
		stem = 'https://m.signalvnoise.com/'
		sentences = []

		for id in ids:
			url = stem + id
			print url
			soup = BeautifulSoup(requests.get(url).text)
			first_block = soup.select('div.section-inner p')[0].text.encode('utf-8')
			first_sentence = re.match(self.first_sentence_regex, first_block).group(0).strip()
			print '%s\n' % first_sentence
			sentences.append((url, first_sentence))
		self.__export(sentences, 'medium')

	# def run(self):
	# 	self.col.insert(
	# 		{
	# 			'help': 'me'
	# 		}
	# 	)
	# 	print self.col.count()

if __name__ == '__main__':
	g = Genesis()
	g.medium()