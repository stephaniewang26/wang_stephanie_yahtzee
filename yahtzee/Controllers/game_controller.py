from flask import Flask
from flask import request
from flask import render_template
import json
import calendar
import math
import os

from Models import Game_Model
DB_location=f"{os.getcwd()}/yahtzee/Models/yahtzeeDB.db"
Games = Game_Model.Game(DB_location, "games")

import html_titles
titles_dict = html_titles.get_titles()

def games_username(username):
    print(f"request.url={request.url}")
    return render_template('user_games.html', title=titles_dict["user_games"], username=username)

def games():
    game_name = request.args.get('game_name_input')
    username = request.args.get('hidden_username')

    Games.create({"name":game_name})

    return render_template('user_games.html', game_name=game_name,username=username)
    