import random
from db import engine
import song_info
import requests

def songs_to_work_on():
	songs = engine.execute("select * from lyrics where genre is NULL limit 100 offset %s", (random.randint(1, 2500)*100,))
	for song in songs:
		yield song

def update_song_info(song):
	info = song_info.get_song_info(song['artist'], song['title'])
	engine.execute("update lyrics set genre=%s where artist=%s and title=%s;", (info['genre'].lower(), song['artist'], song['title']))
	engine.execute('commit')
	print "Set genre for %s - %s to %s" % (song['artist'], song['title'], info['genre'])

def process_song(song):
	print u"checking artist: %s, title: %s".encode('UTF-8') % (song['artist'], song['title'])
	try:
		update_song_info(song)
	except requests.exceptions.HTTPError:
		print "Song not found"
	except song_info.GenreNotFound:
		print "Genre not Found"


if __name__ == '__main__':
	for song in songs_to_work_on():
		process_song(song)

