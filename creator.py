from markov import MarkovChain
import loader

def create_model(genre='country', lookback=3):
	markov = MarkovChain(lookback=lookback)
	for song in loader.songs_to_load(genre=genre):
		for line in song['lyrics']:
			markov.feed(line)
	markov.finalize()
	return markov
