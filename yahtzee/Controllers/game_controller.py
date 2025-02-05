from flask import Flask
from flask import request
from flask import render_template
import json
import calendar
import math
import os

from Models import Game_Model
from Models import Scorecard_Model
from Models import User_Model
DB_location=f"{os.getcwd()}/yahtzee/Models/yahtzeeDB.db"
Games = Game_Model.Game(DB_location, "games")
Scorecards = Scorecard_Model.Scorecard(DB_location, scorecard_table_name="scorecard", user_table_name="users", game_table_name="games")
Users = User_Model.User(DB_location, "users")

import html_titles
titles_dict = html_titles.get_titles()

def games_username(username):
    print(f"request.url={request.url}")

    user_exists_packet = Users.exists(username)
    if user_exists_packet["data"]==False:
        return render_template('login.html',feedback="That user does not exist!",title=titles_dict["login"])

    get_all_packet = Games.get_all()
    all_game_names = []
    for game in get_all_packet["data"]:
        all_game_names.append(game["name"])

    high_scores_list = return_high_scores(username)

    return render_template('user_games.html', high_scores_list=high_scores_list,title=titles_dict["user_games"], username=username, games_list=all_game_names)

def games():
    print(f"request.url={request.url}")
    game_name = request.form.get('game_name')
    username = request.form.get('username')

    create_packet = Games.create({"name":game_name})

    get_all_packet = Games.get_all()
    all_game_names = []
    for game in get_all_packet["data"]:
        all_game_names.append(game["name"])

    # print(all_game_names)
    user_get_packet = Users.get(username=username)
    print(user_get_packet)

    if create_packet["status"] == "success":
        Scorecards.create(game_id=str(create_packet["data"]["id"]), user_id=user_get_packet["data"]["id"], name=f"{game_name}|{username}")
        
        high_scores_list = return_high_scores(username)
        
        return render_template('user_games.html', high_scores_list=high_scores_list, title=titles_dict["user_games"], games_list=all_game_names, username=username, feedback="Game successfully created!")
    else:
        high_scores_list = return_high_scores(username)
        return render_template('user_games.html', high_scores_list=high_scores_list, title=titles_dict["user_games"], games_list=all_game_names, username=username,feedback=create_packet["data"])

def games_game_name_username(game_name,username):
    print(f"request.url={request.url}")
    return render_template('game.html', title=titles_dict["game"]+username,game_name=game_name,username=username)
    
def games_delete_game_name_username(game_name,username):
    print(f"request.url={request.url}")

    scorecards_get_packet_data = (Scorecards.get(name=f"{game_name}|{username}"))["data"]

    remove_packet = Games.remove(game_name=game_name)

    get_all_packet = Games.get_all()
    all_game_names = []
    for game in get_all_packet["data"]:
        all_game_names.append(game["name"])

    high_scores_list = return_high_scores(username)

    if remove_packet["status"] == "success":
        Scorecards.remove(id=scorecards_get_packet_data["id"])
        return render_template('user_games.html', high_scores_list=high_scores_list, title=titles_dict["user_games"], games_list=all_game_names, username=username, feedback="Game successfully removed!")
    else:
        return render_template('user_games.html', high_scores_list=high_scores_list, title=titles_dict["user_games"], games_list=all_game_names, username=username,feedback=remove_packet["data"])
    
def return_high_scores(username):
    print(f"request.url={request.url}")

    all_scores_list = []
    scorecards_get_all_packet_data = Scorecards.get_all()["data"]
    # game_names_list = Scorecards.get_all_user_game_names(username)

    for scorecard in scorecards_get_all_packet_data:
        # print((Games.get(id=scorecard["game_id"]))["data"]["name"])
        print(Games.get(id=int(scorecard["game_id"])))
        if Games.get(id=int(scorecard["game_id"]))["status"]=="success":
            current_game_name = (Games.get(id=int(scorecard["game_id"])))["data"]["name"]

            if scorecard["name"]==(f"{current_game_name}|{username}"):
                all_scores_list.append((current_game_name,(Scorecards.tally_score(scorecard["categories"]))))

    all_scores_list.sort(key=lambda x: x[1],reverse=True)

    return(all_scores_list)

def games_join():
    print(f"request.url={request.url}")
    game_name = request.form.get('game_name')
    username = request.form.get('username')

    exists_packet = Games.create(game_name=game_name)
    #check if game exists
    if exists_packet["data"] == True:
        #check if user has already joined through scorecards
        if 
        Scorecards.create(game_id=str(create_packet["data"]["id"]), user_id=user_get_packet["data"]["id"], name=f"{game_name}|{username}")

    return render_template('user_games.html', title=titles_dict["user_games"])