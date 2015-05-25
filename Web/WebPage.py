#coding:utf-8
__author__ = 'xp'

import time
import datetime
from flask import Flask
from flask import session
from flask import request
from flask import render_template

from OJCodes.Submit import Submit
from OJCodes.PathData import DATA
from OJCodes.DataBaseLinker import DataBaseLinker
from OJCodes.OJDataBaseAdministrator import OJDataBaseAdministrator as OJDBA


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


@app.route('/check', methods=['POST'])
def check():
    if request.method == 'POST':
        userName = request.form['username']
        password = request.form['password']
        data = DataBaseLinker.getInstance().execute("select count(*) as count from Users where user_id='" + userName + "' and user_password='" + password + "'")
        if data[0]['count'] != 0:
            session['username'] = userName
            return render_template('questions.html')
    return 'No data found'


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
    data = DataBaseLinker.getInstance().execute("select * from Question where id =" + str(questionID) + "")
    session['question_id'] = questionID
    return render_template('question.html', questionID=data[0]['id'], questionTIme=data[0]['time'],
                           questionMemory=data[0]['ram'], questionName=data[0]['name'],
                           questionContext=data[0]['context'])


@app.route('/submit')
def submit():
    return render_template('submit.html')


@app.route('/submitCode', methods=['POST'])
def submitCode():
    if request.method == 'POST':
        codeType = request.form['type']
        code = request.form['code']
        if codeType is not None and code is not None:
            now = datetime.datetime.now()
            fileName = DATA.HOST_CODES_PATH + '/' + str(session['username']) + '_' + str(session['question_id']) + '_'\
                       + DATA.getStringTime(str(now)) + '_' + codeType
            # SUBMIT:    user_id, question_id, submit_time, type, codeName, result
            submitDict = {}
            submitDict['user_id'] = str(session['username'])
            submitDict['question_id'] = str(session['question_id'])
            submitDict['submit_time'] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
            submitDict['type'] = codeType
            submitDict['codeName'] = str(session['username']) + '_' + str(session['question_id']) + '_'\
                       + DATA.getStringTime(str(now)) + '_' + codeType
            submitDict['result'] = 'waiting'
            file = open(fileName + '.' + codeType, 'w')
            file.write(code)
            file.close()
            submit = Submit(submitDict)
            OJDBA.addSubmit(submit)
            session.pop('question_id', None)
            return str(codeType) + '    ' + str(code) + submitDict['submit_time']
    return 'No data found'


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()