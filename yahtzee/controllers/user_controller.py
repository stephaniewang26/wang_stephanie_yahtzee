from flask import Flask
from flask import request
from flask import render_template
import json
import calendar
import math
import os

def users():
    print(f"request.url={request.url}")
    if request.method == 'GET':
        return render_template('user_details.html')
    elif request.method == 'POST':
        #pseudocode yayayy
        # import user model
        # get values inputted ✅
        inputted_username = request.form.get("username")
        inputted_password = request.form.get("password")
        inputted_email = request.form.get("email")
        #format to put into user model create ✅
        inputted_info = {"username":inputted_username,
                         "password":inputted_password,
                         "email":inputted_email}
        print(inputted_info)
        # check if user exists (pass in username)
            #if so, return negative feedback
                #return render_template('user_details.html', feedback=negative feedback)
                #you can template in {{feedback}}
            # if not, then attempt to create
                #act depending on if it returns success/error --> if success, then direct to user_games
                #if not, then use feedback from error message and template it in
                    #return render_template('user_details.html', feedback=negative feedback)
        return render_template('user_games.html')

def get_user_details():
    print(f"request.url={request.url}")
    return render_template('user_details.html')

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