# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 10:54:45 2017

@author: HemantKo
"""
import NLTK_StanfordNER_Register as register
import NLTK_StanfordNER_Login as login
import NLTK_StanfordNER_Login_Password as loginpassword

# import the Flask class from the flask module
from flask import Flask, render_template, request

# create the application object
app = Flask(__name__)

question = ""
token = ""
username = ""

# use decorators to link the function to a url
@app.route('/')
def home():
    return render_template('Home.html')  # return a string

@app.route('/Register')
def Register():
    return render_template('Register.html')  # render a template

@app.route('/RegisterUser/', methods=['POST'])
def RegisterUser():
    username = request.form['firstname']
    raw_text = request.form['subject']
    register.start(raw_text,username)
    return render_template('Home.html')

@app.route('/Login')
def Login():
    return render_template('LoginUsername.html')  # render a template

@app.route('/LoginUsername/', methods=['POST'])
def LoginUsername():
    global username
    username = request.form['firstname']
    global question, token 
    question, token = login.start(username)
    return render_template('LoginPassword.html', question = question) 

@app.route('/LoginPassword/', methods=['POST'])
def LoginPassword():
    answer = request.form['answer']
    result = loginpassword.start(answer, token, username)
    return render_template('LoginPassword.html', result = result) 
    
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)