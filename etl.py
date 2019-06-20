import os
import glob
import psycopg2
import json
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    
    """Processes a single song file and stores results
    	 in songs and artists dimension tables
    Args:
        cur(obj): cursor object for executing postgres databases queries
        filepath(str): path to the song file
    		
    Returns:
        nothing
    """
	
    with open(filepath,'r') as f:
        data = f.readline()
        #print(data)
        data = json.loads(data)
  
    df = pd.DataFrame([data])
    print(df)

    # insert song record
    song_data = list(df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0])
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = list(df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    
    """Processes a single log file and stores results in 
    	 time and users dimension tables and in the songplays fact table
    Args:
    	cur(obj): cursor object for executing postgres databases queries
    	filepath(str): path to the song file
    		
    Returns:
    	nothing
    """
    
    with open(filepath, 'r') as f:
        records = f.readlines()
        records = [json.loads(record) for record in records]
    
    df = pd.DataFrame(records)

    # filter by NextSong action
    df_filter = df[df['page']=='NextSong']
    # convert timestamp column to datetime and extract hour, day etc.
    df_filter['ts'] = df_filter.apply(lambda row: pd.to_datetime(row['ts'], unit='ms'), axis=1)
    df_filter['hour'] = df_filter['ts'].dt.hour
    df_filter['day'] = df_filter['ts'].dt.day
    df_filter['weekofyear'] = df_filter['ts'].dt.weekofyear
    df_filter['month'] = df_filter['ts'].dt.month
    df_filter['year'] = df_filter['ts'].dt.year
    df_filter['weekday'] = df_filter['ts'].dt.weekday
	 
    

    # convert timestamp column to datetime and extract hour, day etc.

    
    # insert time data reco
    time_df = df_filter[['ts', 'hour', 'day', 'weekofyear', 'month', 'year', 'weekday']]
     

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        if row['userId'] =='':
            continue
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df_filter.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (str(row['ts']), int(row['userId']), row['level'], songid, artistid, row['sessionId'], row['location'], row['userAgent'])
        cur.execute(songplay_table_insert, songplay_data)


def get_files(filepath):
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))
    print(all_files)
    
    return all_files
		

def process_data(cur, conn, filepath, func):
    """Processes all files and loads all tables (fact and dimensions)
    Args:
        cur(obj): postgres cursor object
        conn(obj): postgres database connection object
        filepath(str): root fielpath where all files (and subdirectories) are stored
        func(obj): function which defines the processing (eather logfiles or songdata)
    Returns:
        nothing
    """
	
    # get all files matching extension from directory
    all_files = get_files(filepath)
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
