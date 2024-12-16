from flask import Flask
from flask import request
from flask import render_template
import json
import calendar
import math
import os

from Models import User_Model
DB_location=f"{os.getcwd()}/yahtzee/Models/yahtzeeDB.db"
Users = User_Model.User(DB_location, "users")

def users():
    print(f"request.url={request.url}")
    user_details_title = "Yahtzee: User Details"
    user_games_title = "Yahtzee: User Games"

    if request.method == 'GET':
        return render_template('user_details.html', btn_context="create", title=user_details_title)
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
            return render_template('user_details.html', feedback="User already exists!", btn_context="create", title=user_details_title)
        # if not, then attempt to create ✅
        else:
            create_packet = Users.create(inputted_info)
            #act depending on if it returns success/error --> if success, then direct to user_games ✅
            if create_packet["status"] == "success":
                return render_template('user_games.html', title=user_games_title)
            #if not, then use feedback from error message and template it in ✅
            else:
                return render_template('user_details.html', feedback=create_packet["data"], btn_context="create", title=user_details_title)

def users_username(username):
    print(f"request.url={request.url}")
    return render_template('user_details.html', btn_context="update delete")

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