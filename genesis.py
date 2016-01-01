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
				try:
					# can't use % interpolation due to unicode issues. % will automatically use the str() function
					f.write('{}\n{}\n\n'.format(url, sentence))
				except Exception, e:
					print 'EXPORT ERROR!', e
					print 'URL:', url
					print 'SENTENCE:', sentence

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
				first_block = soup.select('div.section-inner p')[0].text.encode('utf-8')
				first_sentence = re.match(self.first_sentence_regex, first_block).group(0).strip()
			except Exception, e:
				try:
					first_block = soup.select('div.section-inner p')[1].text.encode('utf-8')
					first_sentence = re.match(self.first_sentence_regex, first_block).group(0).strip()
				except Exception, e:
					print 'REGEX ERROR'
					print 'First block:', first_block
					flag = raw_input('> ')
					if flag == 'n':
						first_sentence = 'REGEX ERROR'
					elif flag == 'b':
						first_sentence = first_block
					elif flag == 's':
						continue
					else:
						exit(1)

			# hacky robustness; all sentences should have at least an ending punctuation
			if len(first_sentence) <= 1:
				first_sentence = 'REGEX ERROR'

			print '%s\n' % first_sentence
			sentences.append((url, first_sentence))

		print 'Finished processing!'
		self.__export(sentences, 'medium')

	def debug_export(self):
		url = 'https://m.signalvnoise.com/30280c7d5e44'
		first_block = BeautifulSoup(requests.get(url).text).select('div.section-inner p')[0].text.encode('utf-8')
		first_sentence = re.match(self.first_sentence_regex, first_block).group(0).strip()
		with open('test.txt', 'w') as f:
			f.write(first_sentence)

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
