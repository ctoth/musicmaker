"""Parses the country music chart csv file and prints how many we have.
This file was downloaded and converted to csv in excel, with the first blank line at the top being removed.
http://bullfrogspond.com/country_charts.rar

The database needs this index:
CREATE INDEX idx_artists_titles on lyrics(artist, title);
"""
import csv
import sqlite3

def main():
	success = total = 0
	#Tuples of (artist, title)
	songs = set()
	with open('country.csv', 'rb') as fp:
		reader = csv.DictReader(fp)
		for item in reader:
			artist, title = item['Artist'], item['Title']
			artist = artist.decode('latin1')
			title = title.decode('latin1')
			songs.add((artist, title))
	print "Checking %d unique songs" % len(songs)
	db = sqlite3.connect('e:\\lyrics.db')
	cursor = db.cursor()
	for artist, title in songs:
		row = db.execute("select 1 from lyrics where artist=? and title=?", (artist, title)).fetchone()
		if row:
			success += 1
			cursor.execute("update lyrics set genre='country' where artist=? and title=?", (artist, title))
		total += 1
	print "%d/%d" % (success, total)
	db.commit()

if __name__ == '__main__':
	main()
