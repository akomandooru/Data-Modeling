import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    """ Drop the database and create a new database
            Input: 
                None
            Output:
                cur: cursor
                conn: connection
    """         
    # connect to default database
    conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()    
    
    # connect to sparkify database
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()
    
    return cur, conn


def drop_tables(cur, conn):
    """ Drop all tables based on the list of drop table queries
            Input: 
                cur: cursor
                conn: connection
            Output:
                None
    """     
    #Drop tables listed in the drop_table_queries list
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """ Create all tables based on the list of create table queries
            Input: 
                cur: cursor
                conn: connection
            Output:
                None
    """     
    #Create tables listed in the create_table_queries list
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """ Main function called when this script is executed on its own
            Input: 
                None
            Output:
                None
    """      
    #Connect to server, drop existing database, create a new database, and reconnect to the new database
    cur, conn = create_database()
    
    #Drop existing tables
    drop_tables(cur, conn)
    
    #Create new tables in the new database
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()