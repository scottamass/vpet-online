import os
from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import current_user, login_required, login_user
from pymongo import MongoClient
import requests

from blueprints.logic.auth.auth import discord_login

# from app import User
mongo_connect=os.getenv('M_CONNECTION_STRING')
db= MongoClient(mongo_connect)
# Define the Blueprint
new_feature_bp = Blueprint('new_feature', __name__, template_folder='templates')

# Define the route in the Blueprint
@new_feature_bp.route('/app/new-feature')
# @login_required    
def new_feature():
    return render_template('/app/homeTest.html')  # Create this template in the templates folder



# @new_feature_bp.route('/app/login/discord')
# def login_discord():

#     url_discord = os.getenv('APP_DISCORD_URL')
#     print(url_discord)
#     return redirect(url_discord)

# @new_feature_bp.route('/app/login/discord/callback')
# def login_discord_callback():
#     print('----------v2------')
#     code = request.args['code']
#     discord_login(code)
#     return redirect('/app/new-feature')