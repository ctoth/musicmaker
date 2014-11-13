import re
import sys
from collections import defaultdict
from random import random

class MarkovChain(object):

	def __init__(self, lines=None, lookback=2):
		self.markov_map = defaultdict(lambda:defaultdict(int))
		self.lookback = lookback
		if lines is not None:
			for i in lines:
				self.feed(i)

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
	#is iterator-safe.
	def sample(self, items):
		t = 0.0
		rnd = random()
		#beware the rare crash condition: due to floating point errors, it's possible we never hit the random number.
		#The solution is to continually assign next_word in case the loop executes to its conclusion.
		next_word = None
		for k, v in items:
			t += v
			next_word = k
			if rnd < t:
				break
		return next_word

	def generate(self):
		sentence = []
		next_word = self.sample(self.markov_map[''].iteritems())
		while next_word != '':
			sentence.append(next_word)
			next_word = self.sample(self.markov_map[' '.join(sentence[-self.lookback:])].iteritems())
		sentence = ' '.join(sentence)
		return sentence

