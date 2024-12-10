from flask import Flask
from flask import request
from flask import render_template
import json
import calendar
import math
import os

def index():
    print(f"request.url={request.url}")
    return render_template('login.html')

def login():
    print(f"request.url={request.url}")
    username = request.args.get('username')
    password = request.args.get('password')
    return render_template('user_games.html', username=username, password=password)

    # if login successful:
    #     return render_template('user_games.html')
    # else:
    #     return render_template('login.html')