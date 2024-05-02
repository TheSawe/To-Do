from connect_to_db import connection

def valid_data(name, email, password):
    with connection.cursor() as cursor:
            select_all_rows = "SELECT * FROM `to_do_users`"
            cursor.execute(select_all_rows)
            rows = cursor.fetchall()
            names = [''.join(row['name']) for row in rows]
            emails = [''.join(row['email']) for row in rows]
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
     