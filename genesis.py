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
		self.ids = []
		self.first_sentence_regex = r'^.*?[\.!\?…](?:\s|$)'
		self.__import_json()

	def __import_json(self):
		self.ids = json.loads(open('medium-12-30-15.json', 'r').read(), object_pairs_hook=OrderedDict).values()

	def __export(self, tuples, source):
		path = '%s/%s-%s.txt' % (os.path.dirname(os.path.realpath(__file__)), source, str(datetime.now()))
		with open(path, 'w') as f:
			for url, sentence in tuples:
				f.write('%s\n%s\n\n' % (url, sentence))

	def medium(self):
		stem = 'https://m.signalvnoise.com/'
		sentences = []

		# url = 'https://m.signalvnoise.com/8f98ec011862'
		# soup = BeautifulSoup(requests.get(url).text)
		# first_block = soup.select('div.section-inner p')[0].text.encode('utf-8')
		# print first_block
		# first_sentence = re.match(self.first_sentence_regex, first_block).group(0).strip()

		for id in self.ids:
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