# sql_db.py

import sqlite3
from sqlite3 import Error
import random
from datetime import date, timedelta
from tqdm import tqdm
import pandas as pd

DATABASE_NAME = "mydatabase.db"

def create_connection():
    """ Create or connect to an SQLite database """
    conn = None;
    try:
        conn = sqlite3.connect(DATABASE_NAME)
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ Create a table with the specified SQL command """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_data(conn, table_name, data_dict):
    """ Insert a new data into a table """
    columns = ', '.join(data_dict.keys())
    placeholders = ', '.join('?' * len(data_dict))
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cur = conn.cursor()
    cur.execute(sql, list(data_dict.values()))
    conn.commit()
    return cur.lastrowid

def query_database(query):
    """ Run SQL query and return results in a dataframe """
    conn = create_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Create a financial table
def setup_financial_table():
    conn = create_connection()
    sql_create_financial_table = """
    CREATE TABLE IF NOT EXISTS finances (
        id INTEGER PRIMARY KEY,
        date TEXT NOT NULL,
        revenue REAL NOT NULL,
        expenses REAL NOT NULL,
        profit REAL NOT NULL
    );
    """
    create_table(conn, sql_create_financial_table)

    # Insert 100 rows with random data
    start_date = date.today() - timedelta(days=99)
    for i in range(100):
        revenue = random.randint(5000, 20000)  # Random revenue between 5000 and 20000
        expenses = random.randint(1000, 15000)  # Random expenses between 1000 and 15000
        profit = revenue - expenses
        data = {
            "date": start_date + timedelta(days=i),
            "revenue": revenue,
            "expenses": expenses,
            "profit": profit
        }
        insert_data(conn, "finances", data)

    conn.close()

def get_schema_representation():
    """ Get the database schema in a JSON-like format """
    conn = create_connection()
    cursor = conn.cursor()
    
    # Query to get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    db_schema = {}
    
    for table in tables:
        table_name = table[0]
        
        # Query to get column details for each table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        column_details = {}
        for column in columns:
            column_name = column[1]
            column_type = column[2]
            column_details[column_name] = column_type
        
        db_schema[table_name] = column_details
    
    conn.close()
    return db_schema

# This will create the table and insert 100 rows when you run sql_db.py
if __name__ == "__main__":

    # Setting up the financial table
    # setup_financial_table()

    # Querying the database
    # print(query_database("SELECT * FROM finances"))

    # Getting the schema representation
    print(get_schema_representation())