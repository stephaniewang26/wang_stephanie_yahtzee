from flask import Flask
from flask import request
from flask import render_template
import json
import calendar
import math

#test hello

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/game')
def game():
    username_input = request.args.get('username_input')
    return render_template('game.html', username = username_input)


app.run(debug=True)