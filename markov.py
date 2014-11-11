import re
import sys
from collections import defaultdict
from random import random

class MarkovChain(object):

	def __init__(self, lines=None, lookback=2):
		if lines is None:
			lines = []
		self.lines = lines
		self.markov_map = defaultdict(lambda:defaultdict(int))
		self.lookback = lookback

	def feed(self, line):
		line = line.split()
		if len(line) > self.lookback:
			for i in xrange(len(line)+1):
				self.markov_map[' '.join(line[max(0,i-self.lookback):i])][' '.join(line[i:i+1])] += 1

	def finalize(self):
		#Convert map to the word1 -> word2 -> probability of word2 after word1
		for word, following in self.markov_map.items():
			total = float(sum(following.itervalues()))
			for key in following:
				following[key] /= total

	#Typical sampling from a categorical distribution
	def sample(self, items):
		next_word = None
		t = 0.0
		for k, v in items:
			t += v
			if t and random() < v/t:
				next_word = k
		return next_word

	def generate(self):
		sentence = []
		next_word = self.sample(self.markov_map[''].items())
		while next_word != '':
			sentence.append(next_word)
			next_word = self.sample(self.markov_map[' '.join(sentence[-self.lookback:])].items())
		sentence = ' '.join(sentence)
		if sentence in self.lines:
			return self.generate()
		return sentence

