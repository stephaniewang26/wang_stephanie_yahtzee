from flask import Flask
from flask import request
from flask import render_template
import json
import calendar
import math
import os

def user_games():
    print(f"request.url={request.url}")
    return render_template('user_games.html')

def create_game():
    game_name = request.args.get('game_name')
    username = request.args.get('username')
    return render_template('user_games.html', game_name=game_name, username = username)