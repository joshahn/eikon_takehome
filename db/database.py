#/usr/bin/env python

import psycopg2

USERS = "users"
COMPOUNDS = "compounds"
USER_EXPERIMENTS = "user_experiments"

def connect():
    conn = psycopg2.connect(database="eikon",
                            host="postgres",
                            port=5432,
                            user="postgres",
                            password="postgres")
    return conn

def initialize():
    for table in [USERS, USER_EXPERIMENTS, COMPOUNDS]:
        create_table(table)


def create_table(tablename):
    if tablename == USERS:
        query = "CREATE TABLE users (user_id int PRIMARY KEY, name text, email text, signup_date DATE)"
    elif tablename == COMPOUNDS:
        query = "CREATE TABLE compounds (compound_id int PRIMARY KEY, compound_name text, compound_structure text)"
    elif tablename == USER_EXPERIMENTS:
        query = "CREATE TABLE user_experiments (experiment_id int PRIMARY KEY, user_id int, experiment_compounds_ids integer[], experiment_run_time int)"
    else:
        print("Unknown table name: {}".format(tablename))
        query = None
    if query:
        print("Query: {}".format(query))
        conn = connect()
        cur = conn.cursor()
        cur.mogrify(query)    
        conn.commit()
        close(conn)


def close(conn):
    conn.close()


def check_exists(tablename):
    conn = connect()
    cur = conn.cursor()
    cur.execute("select exists(select 1 from information_schema.tables where table_name='{}')".format(tablename))
    val = cur.fetchone()[0]
    close(conn)
    return val


def write_to(objects, tablename):
    if tablename == USERS:
        query = "INSERT into {table} (user_id, name, email, signup_date) VALUES ({0}, '{1}', '{2}', '{3}') on conflict (user_id) do nothing;"
    elif tablename == COMPOUNDS:
        query = "INSERT into {table} (compound_id, compound_name, compound_structure) VALUES ({0}, '{1}', '{2}') on conflict (compound_id) do nothing"
    elif tablename == USER_EXPERIMENTS:
        query = "INSERT into {table} (experiment_id, user_id, experiment_compounds_ids, experiment_run_time) VALUES ({0}, {1}, ARRAY {2}, {3}) on conflict (experiment_id) do nothing"
    else:
        print("Unknown table {}; not used".format(tablename))
        query = None
    if query:
        conn = connect()
        cur = conn.cursor()
        for obj in objects:
            cur.execute(query.format(table=tablename, *obj))
            conn.commit()
        return True
    else:
        return False

def fetch_all(query):
    conn = connect()
    cur = conn.cursor()
    cur.execute(query)
    val = cur.fetchall()
    close(conn)
    print(val)
    return val

def fetch_one(query):
    conn = connect()
    cur = conn.cursor()
    cur.execute(query)
    val = cur.fetchone()
    close(conn)
    return val
