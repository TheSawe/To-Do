from connect_to_db import connection

def valid_data(name, email, password) -> bool:
    with connection.cursor() as cursor:
            select_all_rows = "SELECT * FROM `to_do_users`"
            cursor.execute(select_all_rows)
            rows = cursor.fetchall()
            names = [''.join(row['name']) for row in rows]
            emails = [''.join(row['email']) for row in rows]
    if len(name) >= 3 and '@' in email and '.' in email and len(email) >= 10\
        and len(password) >= 8 and email not in emails and name not in names:
            return True
    return False