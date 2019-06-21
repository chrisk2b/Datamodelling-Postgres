# Purpose of the Repository

This repository contains the results of the "Data Modelling with Postgres" Project which is part of the Data Engineering Nanodegree. Its’s purpose is to give the reviewers access to the code. 

# Summary of the Project
The project deals with a start up called Sparkify which is an online music provider. Sparkify wants to collect and analyze data about its user activities. It is e.g. interested in a detailed understanding of which songs users are currently listening. The user activity data is stored as JSON files in a file system. Currently, the analysists are not able to query and analyze the data in an easy way.

The major part of the project is to design a data model which best suits the analytics needs. Further, an ETL pipeline, which loads and transforms the raw JSON data into the database must be developed. The underlaying database technology is Postgres. Files in the Repository
The repository contains the following files/folders:
# Summary of the Datamodel
The Datamodel is based on a Star Schema an consist of the following tables:

 - **Dimension Tables**:
	 1.  **users** - users of Sparkify
	 
	 ![users dimension table](https://github.com/chrisk2b/Datamodelling-Postgres/blob/master/images/users.PNG)
	 
 
      2.  **songs** - songs in music database
    -   _song_id, title, artist_id, year, duration_
   3. **artists** - artists in music database
    -   _artist_id, name, location, latitude, longitude_
   5.  **time** - timestamps of records in **songplays** (cf. fact tables below) broken down into specific units
    -   _start_time, hour, day, week, month, year, weekday_
 - **Fact Tables**:
    1.  **songplays** - records in log data associated with song plays 

	-   _songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent_

# Files in the Repositoty
The following files/folders are contained in the repository:

 - [sql_queries.py](https://github.com/chrisk2b/Datamodelling-Postgres/blob/master/sql_queries.py): This python file contains all CREATE TABLE statements to create the fact and dimension tables as well as (parametrized) INSER statements which are used during the loading process. These statements are imported and used in the files below.
 - [create_tables.py](https://github.com/chrisk2b/Datamodelling-Postgres/blob/master/create_tables.py): The create_tables.py  creates and connects to the postgres database (which is called sparkifydb), drops already existing tables and create all fact and dimension tables which. The statements defined in sql_queries.py are used for this task. The [etl.py](https://github.com/chrisk2b/Datamodelling-Postgres/blob/master/etl.py) script (see below), polulates these tables with data.
 - [etl.py:](https://github.com/chrisk2b/Datamodelling-Postgres/blob/master/etl.py) This file implemets the ETL process, i.e. extraction of the data from the raw JSON files, the transformation into the start schema and the loading into the tables created with the create_tables.py script.
  - [etl.ipynb](https://github.com/chrisk2b/Datamodelling-Postgres/blob/master/etl.ipynb): This is a notebook which implements the ETL process in a prototypical way for just a sing long and song file. 
 - [data:](https://github.com/chrisk2b/Datamodelling-Postgres/tree/master/data) This folder contains sample data for testing purposes. It consists of two sub-folders for log data and song data.
 - [requirements.txt](https://github.com/chrisk2b/Datamodelling-Postgres/blob/master/requirements.txt): Contains all dependencies, cf. below.
 - [test.ipnb:](https://github.com/chrisk2b/Datamodelling-Postgres/blob/master/test.ipynb) A notebook which is used for testing how the database is populated.

 - *README*: This README.
 
# Packages
The following packages are necessary to run the scripts (cf. the "how to use" section below)

 - os
 - glob
 - psycopg2
 - pandas
 - json
 - datetime

The can be installed by using the requirements.txt file by using the command `pip install -r requirements.txt`


# How to use the Repository

 1. open a terminal an execute `python create_tables.py`. This will create the postgres database and all relevant tables. The database is available under localhost and port  5432. Please node that a database with the name studentdb must already be running under localhost.
 2. execute the command `python etl.py`.  This will start the etl process an populate all tables with data. The star schema is now ready for analytical queries. 

 



