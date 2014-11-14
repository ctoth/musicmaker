from db import engine
import html_stripper

def song_to_list(song_text):
	text = html_stripper.extract_text(song_text)
	text = text.replace('\\n', '\n')
	text = text.replace('\\r', '\r')
	text = text.replace('\r\n\r\n', '\r\n')
	text = text.replace('\r\n', '\n')
	return text.split('\n')

def songs_to_load(genre=None):
	if genre is not None:
		cur = engine.execute('select * from songs where genre=%s', (genre, ), stream_results=True)
	else:		
		cur = engine.execute('select * from songs')
	for i in cur.fetchall():
		res = dict(i)
		res['lyrics'] = song_to_list(res['lyrics'])
		yield  res
