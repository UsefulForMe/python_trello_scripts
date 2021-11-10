import os
import sqlite3
from sqlite3.dbapi2 import Error
import modules.card.card_model as Card
import modules.user.user_model as User

db_file = os.environ.get("DB_NAME")


def create_connection():
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        raise e


def create_table(conn, create_table_sql):
    """create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error:
        print(Error)
        raise Error


def init():
    """create tables"""
    conn = create_connection()
    create_table(conn, Card.sql_create_card_table)
    create_table(conn, User.sql_create_user_table)
