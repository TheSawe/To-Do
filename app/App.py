from flask import Flask, render_template, redirect, url_for, request, make_response
import psycopg2
import sys
sys.path.append('./app/postgre_db')
from config import host, user, password, db_name

sys.path.append('./app/functionality')
from app.functionality.get_date import get_current_date
from app.functionality.valid_data import valid_data
from app.functionality.hash_password import hash


app = Flask(__name__)


@app.route('/register')
def registration():
    if request.cookies.get('personal_data'):
        return redirect('/tasks/today')
    return render_template('start_with.html', identifier=0)

@app.route('/register/<error>')
def error_registration(error):
    return render_template('start_with.html', identifier=0, error=error)


@app.route('/request-to-register', methods=['POST', 'GET'])
def requets_to_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        check_data = valid_data(name=name, email=email, password=password)
        if check_data is True:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                dbname=db_name
            )
            connection.autocommit = True
            with connection.cursor() as cursor:
                insert_query = f"INSERT INTO to_do_users (name, email, password) VALUES ('{name}', '{email}', '{hash(password)}');"
                cursor.execute(insert_query)
                connection.commit()

                create_user_db = f'CREATE TABLE {name} (id SERIAL PRIMARY KEY, task TEXT);'
                cursor.execute(create_user_db)
                connection.close()
            return redirect('/sign-in')
        else:
            return redirect(f'/register/{check_data}')
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
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM to_do_users")
            rows = cursor.fetchall()
            for row in rows:
                if row[0] == name and row[2] == hash(password):
                    return redirect(f'/cookie/{name}/{hash(password)}')
        return redirect('/sign-in')
    else:
        return redirect('/tasks/today')

@app.route('/tasks/today')
def homepage():
    if request.cookies.get('personal_data'):
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            select_rows = f"SELECT * FROM {request.cookies.get('personal_data').split()[0][5:].lower()};"
            cursor.execute(select_rows)
            rows = cursor.fetchall()[::-1]
            connection.close()
        return render_template('main.html', action='Мой день', tasks_length=len(rows), tasks=rows, date=get_current_date())
    else:
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

@app.route('/tasks/search', methods=['POST'])
def search():
    search_req = request.form['search-field']
    if search_req:
        return redirect(f'/tasks/search/{search_req}')
    else:
        return redirect('/tasks/today')
    
@app.route('/tasks/search/<string:req>')
def search_tasks(req):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        dbname=db_name
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
            select_rows = f"SELECT * FROM {request.cookies.get('personal_data').split()[0][5:].lower()} WHERE task ILIKE '%{req}%';"
            cursor.execute(select_rows)
            rows = cursor.fetchall()
            connection.close()
            return render_template('search.html', req=req, tasks_length=len(rows), tasks=rows)

@app.route('/result', methods=['POST'])
def result():
    input_value = request.form['input_value']
    if input_value:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            insert_query = f"INSERT INTO {request.cookies.get('personal_data').split()[0][5:].lower()} (task) VALUES ('{input_value}');"
            cursor.execute(insert_query)
            connection.close()
    return redirect('/tasks/today')


@app.route('/delete-task/<task_route>', methods=['POST'])
def delete_task(task_route):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        dbname=db_name
    )
    connection.autocommit = True
    with connection.cursor() as cursor:
        delete_query = f"DELETE from {request.cookies.get('personal_data').split()[0][5:].lower()} where id={task_route};"
        cursor.execute(delete_query)
        connection.close()
    return redirect('/tasks/today')


@app.errorhandler(404)
def empty(error):
    return render_template('not_found.html', error='404'), 404

