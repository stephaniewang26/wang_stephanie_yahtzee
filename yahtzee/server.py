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

def game():
    return render_template('game.html')

app.run(debug=True)