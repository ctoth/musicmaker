import requests
import lxml.html
import requests_cache
requests_cache.install_cache('lyrics_cache')
import html_to_text
import re

class NotFound(Exception):
	pass

class GenreNotFound(NotFound):
	pass

class SongNotFound(NotFound):
	pass

def get_song_info(artist, title):
	"""Retrieves song info from songlyrics.com and returns
	a dictionary with the genre and lyrics.
	Raises GenreNotFound if no genre could be found for the song. This could also indicate something changed on the site
	to make the genre finding code not work.
Raises SongNotFound if the song is not found
Raises requests.exceptions.HTTPError for anything else"""
	artist = artist.lower().replace(' ','-')
	title = convert_title(title)
	url = 'http://www.songlyrics.com/%s/%s-lyrics/' % (artist, title)
	response = requests.get(url)
	if response.status_code == 404:
		raise SongNotFound("Unable to find song")
	response.raise_for_status()
	tree = lxml.html.fromstring(response.content)
	genre = tree.xpath('//div[@class="pagetitle"]/p[contains(text(), "Genre:")]/a/text()')
	if not genre:
		raise GenreNotFound("No genre found for artist %s title %s" % (artist, title))
	genre = genre[0]
	result = {}
	result['genre'] = genre
	video_link = tree.xpath('//div[@class="video-link"]/a/@href')
	if video_link:
		result['youtube_link'] = video_link[0]
	lyrics = tree.xpath('//p[@id="songLyricsDiv"]')[0]
	lyrics = html_to_text.html_to_text(lyrics).strip('\n')
	result['lyrics'] = lyrics
	return result

apostrophe_re = re.compile(r"\\b'")
def convert_title(title):
	"""Convert title to what songlyrics uses for titles.
	Don't Tell 'Em = don-t-tell-em
	"""
	title = title.lower()
	title = title.replace(' ', '-')
	title = title.replace('#', '')
	title = title.replace("?", "")
	title = apostrophe_re.sub('-', title)
	return title
