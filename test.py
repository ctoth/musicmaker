import os
print os.getpid()
import creator
import song
import time

t1 = time.time()
s = song.Song()
print "Creating model..."
model = creator.create_model(lookback=3, genre='rock')
t2 = time.time()
print "duration:", t2-t1
while True:
	song.add_line_to_song(s, model)

