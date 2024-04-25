import pymysql
import sys

sys.path.append('./mydatabase')

from config import host, user, port, password, db_name


connection = pymysql.connect(
    host=host,
    user=user,
    port=port,
    password=password,
    database=db_name,
    cursorclass=pymysql.cursors.DictCursor
)