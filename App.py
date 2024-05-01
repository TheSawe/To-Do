from flask import Flask, render_template, redirect, url_for, request, make_response
import sys

sys.path.append('./functionality')
from functionality.connect_to_db import connection
from functionality.get_date import get_current_date
from functionality.valid_data import valid_data
from functionality.hash_password import hash


app = Flask(__name__)


@app.route('/register')
def registration():
    if request.cookies.get('personal_data'):
        return redirect('/tasks/today')
    return render_template('start_with.html', identifier=0)


@app.route('/request-to-register', methods=['POST', 'GET'])
def requets_to_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if valid_data(name=name, email=email, password=password):
            with connection.cursor() as cursor:
                insert_query = f"INSERT INTO to_do_users (name, email, password) VALUES ('{name}', '{email}', '{hash(password)}');"
                cursor.execute(insert_query)
                connection.commit()

                create_user_db = f'CREATE TABLE {name} (id INT AUTO_INCREMENT PRIMARY KEY, task VARCHAR(255) NOT NULL);'
                cursor.execute(create_user_db)
            return redirect('/sign-in')
        else:
            return redirect('/register')
    else:
        return redirect('/tasks/today')

@app.route('/sign-in')
def sign_in():
    if request.cookies.get('personal_data'):
        return redirect('/tasks/today')
    return render_template('start_with.html', identifier=1)

@app.route('/request-to-sign-in', methods=['POST', 'GET'])
def request_to_sign_in():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        with connection.cursor() as cursor:
            select_all_rows = "SELECT * FROM `to_do_users`"
            cursor.execute(select_all_rows)
            rows = cursor.fetchall()
            for row in rows:
                if row['name'] == name and row['password'] == hash(password):
                    return redirect(f'/cookie/{name}/{hash(password)}')
        return redirect('/sign-in')
    else:
        return redirect('/tasks/today')
    

@app.route('/tasks/today')
def homepage():
    try:
        with connection.cursor() as cursor:
            select_rows = f"SELECT * FROM `{request.cookies.get('personal_data').split()[0][5:]}`;"
            cursor.execute(select_rows)
            rows = cursor.fetchall()
        return render_template('main.html', action='Мой день', tasks_length=len(rows), tasks=rows, date=get_current_date())
    except:
        return redirect('/sign-in')

@app.route('/', methods=['POST', 'GET'])
def redirect_to_homepage():
    return redirect('/sign-in')

@app.route('/leave-account')
def leave_account():
    res = redirect('/sign-in')
    res.set_cookie('personal_data', '', expires=0)
    return res

@app.route('/cookie/<name>/<password>')
def cookie(name, password):
    res = redirect('/tasks/today')
    res.set_cookie('personal_data', f'name:{name} password:{password}', max_age=60*60*24*15)
    return res



@app.route('/result', methods=['POST'])
def result():
    input_value = request.form['input_value']
    if input_value:
        with connection.cursor() as cursor:
            insert_query = f"INSERT INTO {request.cookies.get('personal_data').split()[0][5:]} (task) VALUES ('{input_value}');"
            cursor.execute(insert_query)
            connection.commit()
    return redirect('/tasks/today')


@app.route('/delete-task/<task_route>', methods=['POST'])
def delete_task(task_route):
    with connection.cursor() as cursor:
        delete_query = f"DELETE from `{request.cookies.get('personal_data').split()[0][5:]}` where id={task_route};"
        cursor.execute(delete_query)
        connection.commit()
    return redirect('/tasks/today')


@app.errorhandler(404)
def empty(error):
    return render_template('not_found.html', error='404'), 404


app.run()
