import os
from flask import request
from flask_login import login_user
from pymongo import MongoClient
import requests
mongo_connect=os.getenv('M_CONNECTION_STRING')
db= MongoClient(mongo_connect)

def discord_login(code):
    from app import User
    
    secret =os.getenv('DISCORD_SECRET')
    client_id = os.getenv('DISCORD_CLIENT')
    uri_redirect = os.getenv('URL_REDIRECT')
    
    token_params = {
            'client_id': client_id,
            'client_secret': secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': f'{uri_redirect}/app/login/discord/callback',
            'scope': 'identify',
            'prompt':'none'
        }
    res= requests.post('https://discord.com/api/oauth2/token',data=token_params)
    data = res.json()
    if 'access_token' in data:
            # Fetch user information using the access token
            user_url = 'https://discord.com/api/users/@me'
            headers = {'Authorization': f'Bearer {data["access_token"]}'}
            user_response = requests.get(user_url, headers=headers)
            user_data = user_response.json()
            #print(user_data)
            did=user_data['id']
            dun=user_data['username']
            print(did)
            query= db.userProfiles.userProfiles.find_one({"auth_id":did})
            if query == None:
                db.userProfiles.userProfiles.insert_one({'auth_id':did,'username':dun,"profilePic":None,"role":"player",'battleTower':0,"money":100,'wins':0,'losses':0})
                query= db.userProfiles.userProfiles.find_one({"auth_id":did})
                user_id = query
                user_id = query['_id']
                user = User(user_id,query['username'],None,query['role'])                
                login_user(user, remember=True)
            else: 
                print('user Exists')
                query= db.userProfiles.userProfiles.find_one({"auth_id":did})
                print(query)
                user_id = query['_id']
                user = User(user_id,query['username'],None,query['role'])                
                login_user(user, remember=True)