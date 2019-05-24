import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """ Read a song file and insert the file contents into the song table and artist table
            Input: 
                cur: cursor
                filepath: input song file in json format
            Output:
                None
    """
    # open song file
    df = pd.read_json(filepath,typ='series')

    # insert song record
    song_data = df[['song_id','title','artist_id','year','duration']].values.tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].values.tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """ Read a log file, filters records by NextSong, and inserts into time table, users table and songplays table
            Input: 
                cur: cursor
                filepath: input log file in json format
            Output:
                None
    """    
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page == 'NextSong']

    # convert timestamp column to datetime
    ts_dt = pd.to_datetime(df['ts'],unit='ms')
    
    # insert time data records
    time_df = pd.DataFrame({'start_time':ts_dt.dt.time,'hour':ts_dt.dt.hour,\
                            'day':ts_dt.dt.day,'week':ts_dt.dt.week,'month':ts_dt.dt.month,\
                            'year':ts_dt.dt.year,'weekday':ts_dt.dt.dayofweek})

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = pd.DataFrame({'user_id':df['userId'],'first_name':df['firstName'], \
                            'last_name':df['lastName'],'gender':df['gender'],'level':df['level']})

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts).time(),\
                         row.userId,row.level,songid,artistid,row.sessionId,row.location,row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """ Iterates over all files in the input filepath recursively and process each file with the input function
            Input: 
                cur: cursor
                conn: connection
                filepath: input file in json format
                func: process function pointer (songs or log processor)
            Output:
                None
    """    

    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """ Main function called when this script is executed on its own
            Input: 
                None
            Output:
                None
    """    
    # Connect to the server
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    # Create cursor
    cur = conn.cursor()
    
    #Process song data files using the process_song_file function
    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    #Process log data files using the process_log_file function
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    # Close connection
    conn.close()

# Call main function if this module is called directly 
if __name__ == "__main__":
    main()