from flask import Flask
from flask import request
from flask import render_template
import json
import calendar
import math
import os

import html_titles
titles_dict = html_titles.get_titles()

def index():
    print(f"request.url={request.url}")
    return render_template('login.html', title=titles_dict["login"])

def login():
    print(f"request.url={request.url}")
    username = request.args.get('username')
    password = request.args.get('password')
    return render_template('user_games.html', username=username, password=password, title=titles_dict["user_games"])

    # if login successful:
    #     return render_template('user_games.html')
    # else:
    #     return render_template('login.html')