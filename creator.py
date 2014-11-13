from markov import MarkovChain
import loader

def create_model(genre=None, lookback=3):
	markov = MarkovChain(lookback=lookback)
	for num, song in enumerate(loader.songs_to_load(genre=genre)):
		if not num % 1000:
			print num
		for line in song['lyrics']:
			markov.feed(line)
	markov.finalize()
	return markov
