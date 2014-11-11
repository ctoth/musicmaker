import creator
import song

s = song.Song()
model = creator.create_model(lookback=3)
while True:
	song.add_line_to_song(s, model)

