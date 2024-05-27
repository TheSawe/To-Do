import psycopg2
import sys
sys.path.append('./app/postgre_db')
from config import host, user, password, db_name

connection = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      dbname=db_name
)

def valid_data(name, email, password):
    with connection.cursor() as cursor:
            select_all_rows = "SELECT * FROM to_do_users"
            cursor.execute(select_all_rows)
            rows = cursor.fetchall()
            connection.close()
            names = [''.join(row[0]) for row in rows]
            emails = [''.join(row[1]) for row in rows]
    if len(name) <= 3:
          return 'short-name'
    elif name in names:
          return 'name-already-using'
    elif email in emails:
          return 'email-already-using'
    elif len(password) <= 8:
          return 'simple-password'
    else:
          return True
