#### Introduction
This repository contains scripts to create database and ETL pipeline for analysing the data collected by an app called Sparkify.

The data resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

#### Requirements for running the scripts:
1. Python 3 with psycopg2 and pandas modules
2. Postgres database installed and running on the machine

#### Description of files:
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

#### Steps to run the scripts:
1. The script create_tables.py has be run using the command **python3 create_tables.py** to create the tables in the database
2. The script etl.py has to be run using the command **python3 etl.py** to read data from json files and insert into the tables
