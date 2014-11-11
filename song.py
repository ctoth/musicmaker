import poetry

class Song(object):
	MIN_SYLLABLES = 6
	MAX_SYLLABLES = 10
	LINES_PER_VERSE = 4

	def __init__(self):
		self.lines = []


	def add_line(self, line):
		self.lines.append(line)

	def can_line_go_next(self, line):
		if len(self.lines) == 1:
			first_line = self.lines[0]
			if lines_rhyme(first_line, line):
				return False
		if len(self.lines) < 2:
			syllables = count_line_syllables(line)
			if syllables < self.MIN_SYLLABLES or syllables > self.MAX_SYLLABLES:
				return False
			return True
		last_important_line = self.lines[-2]
		last_syllables = count_line_syllables(last_important_line)
		if last_syllables != count_line_syllables(line):
			return False
		if not lines_rhyme(last_important_line, line):
			return False
		return True

def count_line_syllables(line):
	words = line.split()
	return sum([poetry.nsyl(word) for word in words])

def lines_rhyme(line1, line2):
	last1 = strip_punctuation(line1.split()[-1])
	last2 = strip_punctuation(line2.split()[-1])
	try:
		return poetry.rhyme(last1, last2)
	except KeyError:
		return False

def add_line_to_song(song, model):
	can_add = False
	while not can_add:
		line = model.generate()
		can_add = song.can_line_go_next(line)
	song.add_line(line)
	print line
	return song

def strip_punctuation(word):
	return ''.join([char for char in word if char.isalpha()])
