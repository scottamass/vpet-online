import os
from flask import Blueprint, redirect, request
from flask_login import login_user
from pymongo import MongoClient

from blueprints.logic.auth.auth import discord_login

# Setup MongoDB Connection
mongo_connect = os.getenv('M_CONNECTION_STRING')
db = MongoClient(mongo_connect)

# Define the Authentication Blueprint
auth_bp = Blueprint('auth', __name__)

# Discord Login URL Redirect
@auth_bp.route('/app/login/discord')
def login_discord():
    url_discord = os.getenv('APP_DISCORD_URL')
    print(url_discord)
    return redirect(url_discord)

# Discord OAuth Callback
@auth_bp.route('/app/login/discord/callback')
def login_discord_callback():
    print('----------v2------')
    code = request.args['code']
    discord_login(code)
    return redirect('/app/new-feature')
