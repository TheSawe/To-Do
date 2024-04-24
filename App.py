from flask import Flask, render_template, redirect, url_for, request, make_response
from db.config import host, user, port, password, db_name
import pymysql
from functionality.get_date import get_current_date


app = Flask(__name__)

connection = pymysql.connect(
    host=host,
    user=user,
    port=port,
    password=password,
    database=db_name,
    cursorclass=pymysql.cursors.DictCursor
)


@app.route('/register')
def registration():
    return render_template('registration.html')


@app.route('/request-to-register', methods=['POST'])
def requets_to_register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    print(f'{name} {email} {password}')
    return redirect('/tasks/today')


@app.route('/tasks/today')
def homepage():
    with connection.cursor() as cursor:
        select_all_rows = "SELECT * FROM `tasks`"
        cursor.execute(select_all_rows)
        rows = cursor.fetchall()
    return render_template('main.html', action='Мой день', tasks_length=len(rows), tasks=rows, date=get_current_date())


@app.route('/', methods=['POST', 'GET'])
def redirect_to_homepage():
    return redirect('/register')

@app.route('/cookie')
def cookie():
    if not request.cookies.get('foo'):
        res = make_response("Setting a cookie")
        res.set_cookie('foo', 'sawe', max_age=60*60)
    else:
        res = make_response(f'Value of cookie is {request.cookies.get("foo")}')
    return res


@app.route('/result', methods=['POST'])
def result():
    input_value = request.form['input_value']
    with connection.cursor() as cursor:
        insert_query = f"INSERT INTO tasks (task) VALUES ('{input_value}');"
        cursor.execute(insert_query)
        connection.commit()
    return redirect('/tasks/today')


@app.route('/delete_task/<task_route>', methods=['POST'])
def delete_task(task_route):
    with connection.cursor() as cursor:
        delete_query = f'DELETE from `tasks` where task="{task_route}";'
        cursor.execute(delete_query)
        connection.commit()
    return redirect('/tasks/today')


@app.errorhandler(404)
def empty(error):
    return render_template('not_found.html', error='404'), 404


app.run()
