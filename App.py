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
            with connection.cursor() as cursor:
                insert_query = f"INSERT INTO to_do_users (name, email, password) VALUES ('{name}', '{email}', '{hash(password)}');"
                cursor.execute(insert_query)
                connection.commit()

                create_user_db = f'CREATE TABLE {name} (id SERIAL PRIMARY KEY, task TEXT);'
                cursor.execute(create_user_db)
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
        with connection.cursor() as cursor:
            connection.rollback()
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
        with connection.cursor() as cursor:
            select_rows = f"SELECT * FROM {request.cookies.get('personal_data').split()[0][5:].lower()};"
            cursor.execute(select_rows)
            rows = cursor.fetchall()[::-1]
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
    print(search_req)
    return redirect('/tasks/today')

@app.route('/result', methods=['POST'])
def result():
    input_value = request.form['input_value']
    if input_value:
        with connection.cursor() as cursor:
            insert_query = f"INSERT INTO {request.cookies.get('personal_data').split()[0][5:].lower()} (task) VALUES ('{input_value}');"
            cursor.execute(insert_query)
    return redirect('/tasks/today')


@app.route('/delete-task/<task_route>', methods=['POST'])
def delete_task(task_route):
    with connection.cursor() as cursor:
        delete_query = f"DELETE from {request.cookies.get('personal_data').split()[0][5:].lower()} where id={task_route};"
        cursor.execute(delete_query)
    return redirect('/tasks/today')


@app.errorhandler(404)
def empty(error):
    return render_template('not_found.html', error='404'), 404

if __name__ == '__main__':
    app.run(debug=False)
