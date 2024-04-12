from flask import Flask, render_template, redirect, url_for, request
from db.config import host, user, port, password, db_name
import pymysql

app = Flask(__name__)

connection = pymysql.connect(
    host=host,
    user=user,
    port=port,
    password=password,
    database=db_name,
    cursorclass=pymysql.cursors.DictCursor
)
print('Succesfully connected!')


@app.route('/tasks/today')
def homepage():
    return render_template('index.html', action='Мой день')


@app.route('/')
def redirect_to_homepage():
    return redirect('/tasks/today')

@app.route('/result', methods=['POST'])
def result():
    input_value = request.form['input_value']
    print(input_value)
    return redirect('/tasks/today')

app.run()
