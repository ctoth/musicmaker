import random
import db


class Robot(object):

	def __init__(self, to_process=1000):
		self.to_process = to_process

	def songs_to_work_on(self):
		songs = db.session.query(db.Song).filter(db.Song.genre == None).limit(self.to_process).offset(random.randint(1, 100) * self.to_process)
		for song in songs:
			yield song

	def process_song(self, song):
		info = self.get_song_info(song)
		song.update(info)
		db.session.add(song)
		db.session.commit()

	def get_song_info(self):
		raise NotImplementedError

	def run(self):
		for song in self.songs_to_work_on():
			msg = u"checking artist: %s, title: %s".encode('UTF-8') % (song.artist.name, song.title)
			print msg.encode('UTF-8')
			try:
				self.process_song(song)
			except Exception as e:
				print e.message

