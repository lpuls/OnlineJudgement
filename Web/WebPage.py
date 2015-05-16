#coding:utf-8
__author__ = 'xp'

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/do')
def hello():
    return 'Hello World'

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/aboutme')
def aboutme():
    return render_template('aboutMe.html')

@app.route('/questions')
def questions():
    return render_template('questions.html')

@app.route('/question/<questionID>')
def question(questionID):
    return questionID


if __name__ == '__main__':
    app.debug = True
    app.run()