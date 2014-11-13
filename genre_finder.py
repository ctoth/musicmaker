import random
from db import engine
import song_info

def find_song_to_work_on():
	song = engine.execute("select * from lyrics where genre is NULL limit 1 offset %s", (random.randint(1, 250),)).fetchone()
	return song

def update_song_info(song):
	info = song_info.get_song_info(song['artist'], song['title'])
	engine.execute("update lyrics set genre='%s' where artist='%s' and title='%s';", (info['genre'], song['artist'], song['title']))
	engine.execute('commit')
	print "Set genre for %s - %s to %s" % (song['artist'], song['title'], info['genre'])


if __name__ == '__main__':
	update_song_info(find_song_to_work_on())