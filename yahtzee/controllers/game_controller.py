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
