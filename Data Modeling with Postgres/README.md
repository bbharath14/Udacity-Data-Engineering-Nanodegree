### Introduction
This repository contains scripts to create database and ETL pipeline for analysing the data collected by an app called Sparkify.

The data resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

### Database Schema
The schema used for this exercise is the star schema with one fact(songplays) table and four dimension tables which are users, songs, artists and time.

#### Fact table
songplays - records in log data associated with song plays i.e. records with page NextSong

* songplay_id (SERIAL) PRIMARY KEY: ID of each user song play
* start_time (TIMESTAMP) NOT NULL: Timestamp of beginning of user activity
* user_id (INT) NOT NULL: ID of user
* level (VARCHAR): User level {free | paid}
* song_id (VARCHAR): ID of Song played
* artist_id (VARCHAR): ID of Artist of the song played
* session_id (INT) NOT NULL: ID of the user Session
* location (VARCHAR): User location
* user_agent (VARCHAR): Agent used by user to access Sparkify platform

#### Dimension Tables
users - users of the app

* user_id (INT) PRIMARY KEY: ID of user
* first_name (VARCHAR) NOT NULL: Name of user
* last_name (VARCHAR) NOT NULL: Last Name of user
* gender (VARCHAR): Gender of user {M | F}
* level (VARCHAR): User level {free | paid}

songs - songs in music database

* song_id (VARCHAR) PRIMARY KEY: ID of Song
* title (VARCHAR) NOT NULL: Title of Song
* artist_id (VARCHAR) NOT NULL: ID of song artist
* year (INT): Year of song release
* duration (FLOAT) NOT NULL: Song duration in milliseconds

artists - artists in music database

* artist_id (VARCHAR) PRIMARY KEY: ID of artist
* name (VARCHAR) NOT NULL: Name of artist
* location (VARCHAR): Location of the artist
* lattitude (FLOAT): Lattitude location of artist
* longitude (FLOAT): Longitude location of artist

time - timestamps of records in songplays broken down

* start_time (TIMESTAMP) PRIMARY KEY: Timestamp of row
* hour (INT): Hour of the start_time
* day (INT): Day of the start_time
* week (INT): Week of the start_time
* month (INT): Month of the start_time
* year (INT): Year of the start_time
* weekday (VARCHAR): Name of week day associated to start_time

### Requirements for running the scripts:
1. Python 3 with psycopg2 and pandas modules
2. Postgres database installed and running on the machine

### Description of files:
1. The script create_tables.py does the following:
    1. Drops (if exists) and Creates the sparkify database.
    2. Establishes connection with the sparkify database and gets cursor to it.  
    3. Drops all the tables and creates all the tables needed
    4. Finally, closes the connection.
    
2. The script etl.py contains the steps for extract, transform and load pipeline. It does the following:
    1. iterates the directory to get list of all json files
    2. extracts the needed data from json files in song_data and inserts in songs and artists tables
    3. extracts the needed data from json files in log_data and inserts in time, users and song_plays tables
    
3. The script sql_queries.py contains the list of queries used to create/drop the tables and to inserts and read data from the tables. This
script is used internally in other scripts and shouldn't be run separately

### Steps to run the scripts:
1. The script create_tables.py has be run using the command **python3 create_tables.py** to create the tables in the database
2. The script etl.py has to be run using the command **python3 etl.py** to read data from json files and insert into the tables
