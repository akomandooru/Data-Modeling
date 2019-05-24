# string constants for the various drop table statements
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# songplays table create script has a primary key on songplay_id (serial type - autogenerated/incremented number) and
# all other columns set to be non nullable fields
songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (songplay_id SERIAL PRIMARY KEY, \
                         start_time time NOT NULL, user_id int NOT NULL, \
                         level varchar NOT NULL, song_id varchar references songs(song_id), \
						 artist_id varchar references artists(artist_id), session_id int  NOT NULL, \
                         location varchar NOT NULL, user_agent varchar NOT NULL);""")

# users table create script has a primary key on user_id with other columns set to be non null
# gender column is set with a constraint so it can only take two values 'M' or 'F'
user_table_create = ("""CREATE TABLE IF NOT EXISTS users (user_id int PRIMARY KEY, first_name varchar NOT NULL, \
					 last_name varchar NOT NULL, \
                     gender varchar NOT NULL CONSTRAINT just_one_char CHECK (gender in ('M','F')), \
                     level varchar NOT NULL);""")    

# songs table create script has a primary key on song_id; other columns are are set to not null
song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (song_id varchar PRIMARY KEY, title varchar NOT NULL, \
                    artist_id varchar NOT NULL, year int NOT NULL, duration numeric NOT NULL);""")

# artists table create script has a primary key on artist_id; other columns are not null except for lattitude and longitude
# lattitude and longitude are set to be nullable due to the input files have null values for these fields
artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (artist_id varchar PRIMARY KEY, \
                       name varchar NOT NULL,location varchar NOT NULL,lattitude numeric, \
                       longitude numeric);""")

# time table create script has a primary key on all fields here as this table splits a timestamp and stores the different parts in it
time_table_create = ("""CREATE TABLE IF NOT EXISTS time (start_time time NOT NULL, hour int NOT NULL, \
                    day int NOT NULL, week int NOT NULL, \
                    month int NOT NULL, year int NOT NULL, weekday int NOT NULL, \
                    PRIMARY KEY (start_time, hour, day, week, month, year, weekday));""")

# songplays insert script; each insert on this table will be unique due to the SERIAL songplay_id column
songplay_table_insert = ("""INSERT INTO songplays (start_time, user_id, level, \
                         song_id,\
						 artist_id, session_id, location, user_agent) \
						 VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""")

# users insert script; when there is a conflict on user_id, we update the existing record with the new record values
user_table_insert = ("""INSERT INTO users (user_id, first_name, \
					 last_name, gender, level) \
					 VALUES (%s,%s,%s,%s,%s) \
                     ON CONFLICT (user_id) DO UPDATE SET \
                     level=EXCLUDED.level""")

# songs insert script; when there is a conflict on song_id, we update existing record with the new record values
song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration) \
					 VALUES (%s,%s,%s,%s,%s)\
                     ON CONFLICT (song_id)  DO NOTHING""")

# artists insert script; when there is a conflict on artist_id, we update existing record with the new record values
artist_table_insert = ("""INSERT INTO artists (artist_id,name,location,lattitude, longitude) \
					 VALUES (%s,%s,%s,%s,%s) \
                     ON CONFLICT (artist_id)  DO NOTHING""")

# time insert script; when there is a conflict due to a duplciate row, we ignore it
time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday) \
					 VALUES (%s,%s,%s,%s,%s,%s,%s) \
                     ON CONFLICT (start_time, hour, day, week, month, year, weekday) DO NOTHING""")

# find songs script that will return the song_id and artist_id for a given song title, artist name, and song duration
song_select = ("""select song_id,artists.artist_id from songs join artists on songs.artist_id=artists.artist_id \
				  where songs.title=%s and artists.name=%s and songs.duration=%s""")

# list of create table scripts; 
create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create,songplay_table_create]
# list of drop table scripts;
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]