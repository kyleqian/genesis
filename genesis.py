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
		self.first_sentence_regex = r'^.*?[\.!\?…](?:\s|$|"|”)'

	# imports list of article IDs, returns list of IDs
	def __import_json(self, filename):
		return json.loads(open(filename, 'r').read(), object_pairs_hook=OrderedDict).values()

	# exports txt file
	# TODO: add to mongo
	def __export(self, tuples, source):
		print 'Exporting %d items...' % len(tuples)
		path = '%s/%s-%s.txt' % (os.path.dirname(os.path.realpath(__file__)), source, str(datetime.now()))
		with open(path, 'w') as f:
			for url, sentence in tuples:
				f.write('%s\n%s\n\n'.encode('utf-8') % (url, sentence))

	# medium articles
	def medium(self):
		ids = self.__import_json('medium-12-30-15.json')
		stem = 'https://m.signalvnoise.com/'
		sentences = []
		count = 0

		for id in ids:
			url = stem + id
			print url
			soup = BeautifulSoup(requests.get(url).text)

			try:
				for i in xrange(2):
					first_block = soup.select('div.section-inner p')[i].text.encode('utf-8')
					first_sentence = re.match(self.first_sentence_regex, first_block).group(0).strip()
			except Exception, e:
				if i == 1:
					print 'REGEX ERROR!'
					print 'First block:', first_block
					if raw_input('>') == 'n':
						continue
					else:
						exit(1)
				else:
					pass

			print '%s\n' % first_sentence
			sentences.append((url, first_sentence))

		print 'Finished processing!'
		self.__export(sentences, 'medium')

	def __insert_test(self):
		self.col.insert(
			{
				'help': 'me'
			}
		)
		print self.col.count()

if __name__ == '__main__':
	g = Genesis()
	g.medium()