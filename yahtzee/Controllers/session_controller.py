from flask import Flask
from flask import request
from flask import render_template
import json
import calendar
import math
import os


from Models import User_Model
from Models import Game_Model
from Models import Scorecard_Model
DB_location=f"{os.getcwd()}/yahtzee/Models/yahtzeeDB.db"
Users = User_Model.User(DB_location, "users")
Games = Game_Model.Game(DB_location, "games")
Scorecards = Scorecard_Model.Scorecard(DB_location, scorecard_table_name="scorecard", user_table_name="users", game_table_name="games")

import html_titles
titles_dict = html_titles.get_titles()

import game_controller

def index():
    print(f"request.url={request.url}")
    return render_template('login.html', title=titles_dict["login"])

def login():
    print(f"request.url={request.url}")
    username = request.args.get('username')
    password = request.args.get('password')

    if (Users.exists(username=username))["data"] != True:
        return render_template('login.html', feedback="That user does not exist!",title=titles_dict["login"])

    get_packet_data = (Users.get(username=username))["data"]

    if password == get_packet_data["password"]:
        all_game_names = game_controller.get_user_game_names(username)

        high_scores_list = game_controller.return_high_scores(username)

        return render_template('user_games.html', high_scores_list=high_scores_list, games_list=all_game_names, username=username, password=password, title=titles_dict["user_games"])
    else:
        return render_template('login.html',feedback="Incorrect password.",title=titles_dict["login"])