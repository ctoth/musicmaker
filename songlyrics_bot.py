import songlyrics
import robot

class SonglyricsRobot(robot.Robot):

	def get_song_info(self, song):
		info = songlyrics.get_song_info(song.artist.name, song.title)
		info['genre'] = info['genre'].lower()
		return info

if __name__ == '__main__':
	bot = SonglyricsRobot()
	bot.run()
