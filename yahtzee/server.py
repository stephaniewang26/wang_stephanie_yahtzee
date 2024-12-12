from flask import Flask
from flask import request
from flask import render_template
import os
import sys
import json
import calendar
import math

app = Flask(__name__, static_url_path='', static_folder='static')

#Connect Controller definitions
fpath = os.path.join(os.path.dirname(__file__), 'controllers')
sys.path.append(fpath)
fpath = os.path.join(os.path.dirname(__file__), 'models')
sys.path.append(fpath)
from Controllers import session_controller, game_controller, user_controller

#The Router section of our application conects routes to Contoller methods

#SESSION
app.add_url_rule('/', view_func=session_controller.index, methods = ['GET'])
app.add_url_rule('/login', view_func=session_controller.login, methods = ['GET'])

#GAME
app.add_url_rule('/games/<username>', view_func=game_controller.user_games, methods = ['GET'])
app.add_url_rule('/games', view_func=game_controller.create_game, methods = ['POST'])
# app.add_url_rule('/games/join', view_func=game_controller.join_game, methods = ['POST'])
# app.add_url_rule('/games/delete/<game_name>/<username>', view_func=game_controller.remove_user_from_game, methods = ['GET'])
# app.add_url_rule('/games/<game_name>/<username>', view_func=game_controller.get_game, methods = ['GET'])

#SCORECARD

#USER
app.add_url_rule('/users', view_func=user_controller.blank_user_details, methods = ['POST', 'GET'])
app.add_url_rule('/users/<username>', view_func=user_controller.get_user_details, methods = ['GET'])

# app.add_url_rule('/fruit', view_func=FruitController.fruit, methods = ['POST', 'GET'])
# app.add_url_rule('/fruit/<fruit_name>', view_func=FruitController.single_fruit, methods = ['GET'])




# @app.route('/')
# def login():
#     return render_template('login.html')

# @app.route('/game')
# def game():
#     username = request.args.get('username')
#     return render_template('game.html', username = username)

#START SERVER
if __name__=="__main__":
    port = int(os.environ.get("PORT",8080))
    app.run(debug=True, port=port)