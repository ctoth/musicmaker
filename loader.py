import sqlite3
import html_stripper

def song_to_list(song_text):
	text = html_stripper.extract_text(song_text)
	text = text.replace('\\n', '\n')
	text = text.replace('\\r', '\r')
	text = text.replace('\r\n\r\n', '\r\n')
	text = text.replace('\r\n', '\n')
	return text.split('\n')

def songs_to_load(genre='country'):
	con = sqlite3.connect('e:\\lyrics.db')
	con.row_factory = sqlite3.Row
	cur = con.execute('select * from lyrics where genre=?', (genre, ))
	for i in cur.fetchall():
		res = dict(i)
		res['lyrics'] = song_to_list(res['lyrics'])
		yield  res
