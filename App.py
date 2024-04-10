from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/tasks/today')
def homepage():
    return render_template('index.html', action='Мой день')


@app.route('/')
def redirect_to_homepage():
    return redirect('/tasks/today')


app.run()
