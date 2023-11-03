import json
import datetime
from flask import Flask, Response, flash, jsonify, redirect, request,session , render_template, url_for
from flask_login import LoginManager, UserMixin, login_required,login_user,current_user, logout_user
from flask_bcrypt import Bcrypt
from pymongo import DESCENDING, MongoClient
from bson import json_util,ObjectId
import os
from functions.dbfunct import evocheck, fetch_player_monster, give_monster_to_player



mongo_connect=os.getenv('M_CONNECTION_STRING')
print(mongo_connect)
db= MongoClient(mongo_connect)

VERSION='0.5'

class User(UserMixin):
    def __init__(self,id,username,pic,role):
        
        self.id = id
        self.username = username
        self.pic = pic
        self.roles=role

class Post():
    def __init__(self,monsterid,poster_id, posted_date):
        self.game = monsterid 
        self.poster_id=poster_id
        self.posted_date = posted_date

    

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

login_manager = LoginManager()

@login_manager.unauthorized_handler
def unauthenticated():
        
        return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    u= db.userProfiles.userProfiles.find_one({'_id':ObjectId(user_id)})
    if u is not None:
        return User(id=u['_id'],username=u['username'],pic=u['profilePic'],role=u['role'])

login_manager.init_app(app)

def parse_json(data):
    return json.loads(json_util.dumps(data))


@app.route('/')
def index():
 
    return render_template('home.html')
    

@app.route('/player')
@login_required
def player():
    monster=fetch_player_monster(current_user.id)
    if monster != None:
        evocheck(current_user.id)
        monster=fetch_player_monster(current_user.id)
    backgroundUrl='/static/bg/1.jpeg'
    
    return render_template('playersummary.html' ,monster=monster ,backgroundUrl=backgroundUrl) 

@app.route('/api/createmonster', methods=['POST'])
@login_required
def post_game():
    
    game = request.form.get('options')
    poster_id = current_user.id
    posted_date = datetime.datetime.now()
    newmonster = Post(game,poster_id,posted_date)
    give_monster_to_player(newmonster)
    return redirect(url_for('index'))
    







    

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email= request.form ['email']
        user = request.form ['username']
        pw= request.form ['pwd']
        if db.authDb.users.find_one({"email":email}):
            return "user in db"
        elif db.authDb.users.find_one({"username":user}):    
            return "username exists"
        else: 
            hashed_pw = bcrypt.generate_password_hash(pw)
            db.authDb.users.insert_one({"email":email,"password":hashed_pw,'username':user})
            requested_user = db.authDb.users.find_one({"email":email})
            print(requested_user)
            user_uid = requested_user["_id"]
            #add user to profile db
            db.userProfiles.userProfiles.insert_one({'auth_id':user_uid,'username':user,"profilePic":None,"role":"player"})
            return redirect(url_for('login'))
    else: return render_template("register.html")            

@app.route('/login',methods=['POST','GET'] )
def login():
    if request.method == 'POST':
        user = request.form ['username']
        pw= request.form ['pwd']
        query= db.authDb.users.find_one({"email":user})
        if db.authDb.users.find_one({"email":user}):
            if bcrypt.check_password_hash(query['password'],pw):                
                user_name=db.userProfiles.userProfiles.find_one({"auth_id":ObjectId(query['_id'])})
                user_id = user_name['_id']
                user = User(user_id,user_name['username'],None,user_name['role'])                
                login_user(user, remember=True)
                return redirect('/')
            else: 
                flash('Incorrect email or password please try again ')
                return redirect('/login')
        else: 
            flash('Incorrect email or password please try again ')
            return redirect('/login')
    else: return render_template("login.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/api/register', methods=['GET','POST'])
def api_register():
    if request.method == 'POST':
        user=request.json["email"]
        pw=request.json["password"]
        print(user)
        if db.loginUsers.created_users.find_one({"email":user}):
            return "user in db"
        else: 
            hashed_pw = bcrypt.generate_password_hash(pw)
            db.loginUsers.created_users.insert_one({"email":user,"password":hashed_pw})
            requested_user = db.loginUsers.created_users.find_one({"email":user})
            user_uid = requested_user["_id"]
            print(user_uid)
            return redirect(url_for('login'))
    else: return render_template("register.html")       


@app.route('/api/login',methods=['POST','GET'] )
def api_login():
    if request.method == 'POST':
        user=request.json["email"]
        pw=request.json["password"]
        query= db.loginUsers.created_users.find_one({"email":user})
        if db.loginUsers.created_users.find_one({"email":user}):
            print('user in db')                        
            if bcrypt.check_password_hash(query['password'],pw):               
                user_name=db.loginUsers.created_users.find_one({"email":user})
                user_id = user_name['_id']
                print(user_id)
                user = User(user_id,user_name['email'],None)              
                login_user(user)
                return "200"
            else: return jsonify({"error":"unauthorized"}),401
        else: return jsonify({"error":"unauthorized"}),401
    else: return render_template("login.html")    

if __name__=="__main__":
    app.run(debug=True ,host='0.0.0.0' ,port='80')