--Takes the originally imported lyrics database,
--and creates the needed indexes and columns for parse_csv.
alter table lyrics add column genre text;
CREATE INDEX idx_artists_titles on lyrics(artist, title);
CREATE INDEX idx_genre on lyrics(genre);
