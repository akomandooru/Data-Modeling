# Project: Sparkify ETL
This project delivered an ETL tool for Sparkify so that their data engineering team can support running queries from analytics team.

## ETL Tool: Running queries
* Launch a terminal for running your workspace Python scripts
* Run the create tables scripts first - "python create_tables.py"
* Run the ETL script next - "python etl.py"

## Source code
* create_tables.py - this script file is used to connect to a database server and create new tables for this project
* etl.py - this script file is used to go through the data files and load the Fact and Dimension tables 
* sql_queries.py - this is a module file that has SQL script code for creating new tables, dropping tables, inserting data, and finding songs
* etl.ipynb - this is a test notebook for developing ETL code
* test.ipynb - this is a test notebook to look at the database results coming out of the ETL process

## Additional notes:
* In the events log file, the song title is duplicated again and again; when we push this data into the database, we keep an ID of the song in the Fact table called songplays but store the song details in the songs table. This way, we reduce the duplication of song information by keeping a unique set of songs in the songs table and linking it to the Fact table through the song_id field.
* We anticipate duplicate time values in this scenario as multiple users could start listening to the songs at the same exact moment; in this case, multiple event log entries will have the same timestamp entry. We handle this duplicate values by ignoring duplicates in the time table across its multiple fields.

## Fact and Dimension tables picture
[Tables Picture](https://drive.google.com/file/d/1DeIz6PCJRfsi_hqoOLTC3QLRJRrxVfFd/view?usp=sharing)


