import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
from datetime import datetime

songplay_index=0

def process_song_file(cur, filepath):
    """
    - reads song data from the json file
    - gets the required fields for songs and artists table
    - executes the queries to insert data to the tables
    Parameters:
        cur - psycopg2 cursor object
        filepath - path to the json file
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    for value in df.values:
        song_id = value[6]
        artist_id = value[1]
        title = value[7]
        year = int(value[9])
        duration = float(value[8])
        song_data = (song_id, title, artist_id, year, duration)
        cur.execute(song_table_insert, song_data)

        # insert artist record
        artist_name = value[5]
        artist_location = value[4]
        artist_latitude = value[2]
        artist_longitude = value[3]
        artist_data = (artist_id, artist_name, artist_location, artist_latitude, artist_longitude)
        cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    - reads data from the json file
    - filters by NextSong action
    - converts timestamp column to datetime
    - inserts data into the time table
    - gets the required fields and inserts data into users table
    - inserts data into the songplays table
    Parameters:
        cur - psycopg2 cursor object
        filepath - path to the json file
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df["page"]=="NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = []
    for record in t:
        time_data.append([str(record), record.hour, record.day, record.week, record.month, record.year, record.day_name()])
    column_labels = ("start_time", "hour", "day", "week", "month", "year", "weekday")
    time_df = pd.DataFrame.from_records(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        l = tuple(row)
        cur.execute(time_table_insert, l)

    # load user table
    user_df = df[["userId","firstName","lastName","gender","level"]]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        global songplay_index
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (songplay_index, str(pd.to_datetime(row.ts, unit='ms')), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)
        songplay_index += 1

def process_data(cur, conn, filepath, func):
    """
    - iterates the directory to get list of all json files
    - for each json file, call the func with the filepath as the parameter
    Parameters:
        cur - psycopg2 cursor object
        con - psycopg2 connection object
        filepath - path to the directory with json files
        func - function to be called for each file
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
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()