import psycopg2
import sys

sys.path.append('./postgre_db')

from config import host, user, password, db_name


connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    dbname=db_name
)
connection.autocommit = True