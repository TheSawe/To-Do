from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/tasks/today')
def home_page():
    return render_template('index.html', action='Мой день')


@app.route('/')
def page_not_found():
    return redirect('/tasks/today')


app.run()
