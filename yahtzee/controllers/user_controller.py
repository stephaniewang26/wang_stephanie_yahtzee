from flask import Flask
from flask import request
from flask import render_template
import json
import calendar
import math
import os

def blank_user_details():
    print(f"request.url={request.url}")
    return render_template('user_details.html')

def get_user_details():
    print(f"request.url={request.url}")
    return render_template('user_details.html')