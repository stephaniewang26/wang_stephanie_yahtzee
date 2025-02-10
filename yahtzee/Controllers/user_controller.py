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

def users():
    print(f"request.url={request.url}")

    if request.method == 'GET':
        return render_template('user_details.html', btn_context="create", title=titles_dict["user_details"])
    elif request.method == 'POST':
        # get values inputted ✅
        inputted_username = request.form.get("username")
        inputted_password = request.form.get("password")
        inputted_email = request.form.get("email")
        #format to put into user model create ✅
        inputted_info = {"username":inputted_username,
                         "password":inputted_password,
                         "email":inputted_email}
        print(inputted_info)
        # check if user exists (pass in username) --> if so, return negative feedback ✅
        exists_packet = Users.exists(username=inputted_info["username"])
        if exists_packet["data"] == True:
            print("exists!")
            return render_template('user_details.html', feedback="User already exists!", btn_context="create", title=titles_dict["user_details"])
        # if not, then attempt to create ✅
        else:
            create_packet = Users.create(inputted_info)
            #act depending on if it returns success/error --> if success, then direct to user_games ✅
            if create_packet["status"] == "success":
                all_game_names = game_controller.get_user_game_names(username=create_packet["data"]["username"])

                high_scores_list = game_controller.return_high_scores(create_packet["data"]["username"])

                return render_template('user_games.html', high_scores_list=high_scores_list, title=titles_dict["user_games"], games_list=all_game_names, username=create_packet["data"]["username"])
            #if not, then use feedback from error message and template it in ✅
            else:
                return render_template('user_details.html', feedback=create_packet["data"], btn_context="create", title=titles_dict["user_details"])

def users_username(username):
    print(f"request.url={request.url}")

    if (Users.exists(username=username))["data"] != True:
        return render_template('user_details.html', feedback="That user does not exist!", btn_context="create", title=titles_dict["user_details"])

    get_packet_data = (Users.get(username=username))["data"]
    user_id = get_packet_data["id"]

    if request.method == 'GET':
        #get user details page for update/delete, pre-fill text fields
        return render_template('user_details.html', btn_context="update delete", title=titles_dict["user_details"], username_field=get_packet_data["username"], password_field=get_packet_data["password"], email_field=get_packet_data["email"])
    elif request.method == 'POST':
        #update user details
        inputted_username = request.form.get("username")
        inputted_password = request.form.get("password")
        inputted_email = request.form.get("email")
        updated_info = {"username":inputted_username,
                         "password":inputted_password,
                         "email":inputted_email,
                         "id":user_id}
        print(updated_info)
        print(Users.update(user_info=updated_info))
        #if succeeds, render template
        update_packet = Users.update(user_info=updated_info)
        if (update_packet)["status"] == "success":
            return render_template('user_details.html', feedback="User successfully updated!", btn_context="update delete", title=titles_dict["user_details"], username_field=updated_info["username"], password_field=updated_info["password"], email_field=updated_info["email"])
        #else, show bad feedback
        else:
            return render_template('user_details.html', feedback=update_packet["data"], btn_context="update delete", title=titles_dict["user_details"], username_field=get_packet_data["username"], password_field=get_packet_data["password"], email_field=get_packet_data["email"])

def users_delete_username(username):
    print(f"request.url={request.url}")

    if (Users.exists(username=username))["data"] != True:
        return render_template('login.html', title=titles_dict["login"], feedback="That user does not exist!")
    else:
        Users.remove(username=username)
        return render_template('login.html', title=titles_dict["login"], feedback="User successfully deleted.")




# def fruit():
#     print(f"request.method= {request.method} request.url={request.url}")
#     print(f"request.url={request.query_string}")
#     print(f"request.url={request.args.get('name')}") #GET request & query string
#     print(f"request.url={request.form.get('name')}") #POST request & form body

#     # curl "http://127.0.0.1:5000/fruit/"
#     if request.method == 'GET':
#         return jsonify(Fruit.get_all_fruit())
    
#     #curl -X POST -H "Content-type: application/json" -d '{ "name" : "tomato", "url":"https://en.wikipedia.org/wiki/Tomato"}' "http://127.0.0.1:5000/fruit/new"
#     elif request.method == 'POST':
#         return jsonify(Fruit.create_fruit(request.form))